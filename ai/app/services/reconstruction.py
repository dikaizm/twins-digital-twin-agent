"""
MapAnything 3D Reconstruction Service
Real 3D reconstruction using Meta's MapAnything model
"""

import os
import asyncio
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
import torch
from PIL import Image


class MapAnythingReconstructor:
    def __init__(self, workspace_dir: str = "/tmp/reconstruction"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.device = "cuda" if self._check_cuda() else "cpu"
        self.model = None
        self.model_name = "facebook/map-anything"

    def _check_cuda(self) -> bool:
        try:
            return torch.cuda.is_available()
        except:
            return False

    async def _load_model(self) -> None:
        if self.model is None:
            from mapanything.models import MapAnything
            self.model = MapAnything.from_pretrained(self.model_name).to(self.device)
            self.model.eval()

    async def process(
        self,
        image_paths: List[str],
        options: Dict = None
    ) -> Dict:
        options = options or {}
        scene_id = options.get("scene_id", "scene_" + str(hash("".join(image_paths)))[:8])
        workspace = self.workspace_dir / scene_id
        workspace.mkdir(parents=True, exist_ok=True)

        await self._load_model()

        return await self._reconstruct_with_mapanything(image_paths, workspace, options)

    async def _reconstruct_with_mapanything(
        self,
        image_paths: List[str],
        workspace: Path,
        options: Dict
    ) -> Dict:
        from mapanything.utils.image import load_images

        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

        images_dir = workspace / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for i, img_path in enumerate(image_paths):
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img.thumbnail((840, 840), Image.LANCZOS)
                img.save(images_dir / f"image_{i:04d}.jpg", quality=90)

        views = load_images(str(images_dir))

        with torch.no_grad(), torch.cuda.amp.autocast(enabled=True, dtype=torch.float16):
            predictions = self.model.infer(
                views,
                memory_efficient_inference=True,
                minibatch_size=1,
                use_amp=True,
                amp_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
                apply_mask=True,
                mask_edges=True,
                apply_confidence_mask=False,
                confidence_percentile=10,
                use_multiview_confidence=False,
            )

        point_clouds = []
        confs = []
        for pred in predictions:
            pts3d = pred["pts3d"]
            conf = pred["conf"]
            mask = pred["mask"]
            pts3d_np = pts3d[mask.squeeze(-1)].cpu().numpy()
            conf_np = conf[mask.squeeze(-1)].cpu().numpy()
            point_clouds.append(pts3d_np)
            confs.append(conf_np)

        all_pts3d = np.concatenate(point_clouds, axis=0)
        all_conf = np.concatenate(confs, axis=0)

        merged_pcd_path = workspace / "merged_pointcloud.ply"
        self._save_point_cloud(all_pts3d, all_conf, merged_pcd_path)

        mesh_path = workspace / "scene.ply"
        mesh_success = await self._create_mesh_from_points(all_pts3d, mesh_path)

        scene_glb_path = workspace / "scene.glb"
        if mesh_success and mesh_path.exists():
            self._convert_to_glb(str(mesh_path), str(scene_glb_path))

        preview_path = workspace / "preview.png"
        self._create_preview(all_pts3d, preview_path)

        quality = await self._evaluate_scene_quality(all_pts3d, mesh_success)

        return {
            "scene_url": f"/uploads/{scene_id}/scene.glb",
            "metadata_url": f"/uploads/{scene_id}/metadata.json",
            "preview_url": f"/uploads/{scene_id}/preview.png",
            "pointcloud_url": f"/uploads/{scene_id}/merged_pointcloud.ply",
            "equipment_count": self._estimate_equipment_count(all_pts3d),
            "confidence": quality,
            "processing_time": 0.0,
            "point_cloud_points": len(all_pts3d),
            "mesh_vertices": self._count_mesh_vertices(mesh_path) if mesh_path.exists() else 0,
            "n_views": len(image_paths),
            "model": self.model_name
        }

    def _save_point_cloud(self, points: np.ndarray, confidence: np.ndarray, output_path: Path) -> None:
        try:
            import open3d as o3d
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            colors = np.zeros((len(points), 3))
            colors[:, 0] = np.clip(confidence, 0, 1)
            colors[:, 1] = np.clip(1 - np.abs(confidence - 0.5) * 2, 0, 1)
            colors[:, 2] = np.clip(1 - confidence, 0, 1)
            pcd.colors = o3d.utility.Vector3dVector(colors)
            o3d.io.write_point_cloud(str(output_path), pcd)
        except Exception as e:
            print(f"Point cloud save warning: {e}")

    async def _create_mesh_from_points(self, points: np.ndarray, mesh_path: Path) -> bool:
        try:
            import open3d as o3d
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

            distances = pcd.compute_nearest_neighbor_distance()
            avg_dist = np.mean(distances)
            radii = [avg_dist * 1.5, avg_dist * 3, avg_dist * 6]

            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))
            mesh.compute_vertex_normals()

            o3d.io.write_triangle_mesh(str(mesh_path), mesh)
            return True
        except Exception as e:
            print(f"Mesh creation warning: {e}")
            return False

    def _convert_to_glb(self, ply_path: str, glb_path: str) -> bool:
        try:
            import trimesh
            mesh = trimesh.load(ply_path)
            mesh.export(glb_path, file_type="glb")
            return True
        except Exception as e:
            print(f"GLB conversion warning: {e}")
            return False

    def _create_preview(self, points: np.ndarray, output_path: Path) -> None:
        try:
            import open3d as o3d
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points[:min(len(points), 5000)])

            pcd.paint_uniform_color([0.5, 0.5, 0.5])
            vis = o3d.visualization.Visualizer()
            vis.create_window(visible=False, width=640, height=480)
            vis.add_geometry(pcd)
            vis.poll_events()
            vis.capture_screen_image(str(output_path))
            vis.destroy_window()
        except Exception as e:
            print(f"Preview generation warning: {e}")

    async def _evaluate_scene_quality(self, points: np.ndarray, has_mesh: bool) -> float:
        if len(points) < 100:
            return 0.2

        centroid = np.mean(points, axis=0)
        distances = np.linalg.norm(points - centroid, axis=1)

        std_dist = np.std(distances)
        mean_dist = np.mean(distances)

        if mean_dist > 0:
            uniformity = min(std_dist / mean_dist, 1.0)
        else:
            uniformity = 0.5

        coverage_score = min(len(points) / 5000, 1.0)

        quality = uniformity * 0.4 + coverage_score * 0.3 + (0.8 if has_mesh else 0.4)

        return round(min(max(quality, 0.1), 0.95), 2)

    def _estimate_equipment_count(self, points: np.ndarray) -> int:
        if len(points) < 50:
            return 1

        centroid = np.mean(points, axis=0)
        max_dist = np.max(np.linalg.norm(points - centroid, axis=1))

        estimated_area = np.pi * (max_dist ** 2)
        equipment_density = 0.05
        estimated = max(1, int(estimated_area * equipment_density))

        return min(estimated, 50)

    def _count_mesh_vertices(self, mesh_path: Path) -> int:
        try:
            if not mesh_path.exists():
                return 0
            import open3d as o3d
            mesh = o3d.io.read_triangle_mesh(str(mesh_path))
            return len(mesh.vertices)
        except:
            return 0


def export_to_glb(mesh_path: str, output_path: str) -> bool:
    try:
        import trimesh
        mesh = trimesh.load(mesh_path)
        mesh.export(output_path, file_type="glb")
        return True
    except Exception as e:
        print(f"GLB export error: {e}")
        return False


def create_preview_image(scene_path: str, output_path: str, resolution: Tuple[int, int] = (640, 480)) -> bool:
    try:
        import open3d as o3d
        mesh = o3d.io.read_triangle_mesh(scene_path)
        vis = o3d.visualization.Visualizer()
        vis.create_window(visible=False, width=resolution[0], height=resolution[1])
        vis.add_geometry(mesh)
        vis.poll_events()
        vis.capture_screen_image(output_path)
        vis.destroy_window()
        return True
    except Exception as e:
        print(f"Preview generation error: {e}")
        return False
