# Copyright (c) SI-Analytics. All rights reserved.
from abc import ABCMeta

import torch
from ray.air.config import ScalingConfig
from ray.train.data_parallel_trainer import DataParallelTrainer

from siatune.tune import MMBackendConfig
from .base import BaseTask
from .builder import TASKS


@TASKS.register_module()
class MMBaseTask(BaseTask, metaclass=ABCMeta):
    """Wrap the apis of open mm train-based projects."""

    def create_trainable(self) -> DataParallelTrainer:
        """Get a :class:`DataParallelTrainer` instance.

        Returns:
            DataParallelTrainer: Trainer to optimize hyperparameter.
        """

        return DataParallelTrainer(
            self.context_aware_run,
            backend_config=MMBackendConfig(),
            scaling_config=ScalingConfig(
                trainer_resources=dict(CPU=self.num_cpus_per_worker),
                num_workers=self.num_workers,
                use_gpu=torch.cuda.is_available()))
