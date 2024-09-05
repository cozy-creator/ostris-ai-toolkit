import argparse
from collections import OrderedDict

import torch

from ostris_ai_toolkit.toolkit.config_modules import ModelConfig
from ostris_ai_toolkit.toolkit.stable_diffusion_model import StableDiffusion


parser = argparse.ArgumentParser()
parser.add_argument(
    'input_path',
    type=str,
    help='Path to original sdxl model'
)
parser.add_argument(
    'output_path',
    type=str,
    help='output path'
)
parser.add_argument('--sdxl', action='store_true', help='is sdxl model')
parser.add_argument('--refiner', action='store_true', help='is refiner model')
parser.add_argument('--ssd', action='store_true', help='is ssd model')
parser.add_argument('--sd2', action='store_true', help='is sd 2 model')

args = parser.parse_args()
device = torch.device('cpu')
dtype = torch.float32

print(f"Loading model from {args.input_path}")

if args.sdxl:
    adapter_id = "latent-consistency/lcm-lora-sdxl"
if args.refiner:
    adapter_id = "latent-consistency/lcm-lora-sdxl"
elif args.ssd:
    adapter_id = "latent-consistency/lcm-lora-ssd-1b"
else:
    adapter_id = "latent-consistency/lcm-lora-sdv1-5"


diffusers_model_config = ModelConfig(
        name_or_path=args.input_path,
        is_xl=args.sdxl,
        is_v2=args.sd2,
        is_ssd=args.ssd,
        dtype=dtype,
    )
diffusers_sd = StableDiffusion(
    model_config=diffusers_model_config,
    device=device,
    dtype=dtype,
)
diffusers_sd.load_model()


print(f"Loaded model from {args.input_path}")

diffusers_sd.pipeline.load_lora_weights(adapter_id)
diffusers_sd.pipeline.fuse_lora()

meta = OrderedDict()

diffusers_sd.save(args.output_path, meta=meta)


print(f"Saved to {args.output_path}")
