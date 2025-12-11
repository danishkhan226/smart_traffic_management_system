"""
Diagnostic script to check PyTorch GPU availability
"""
import sys

print("=" * 70)
print("PYTORCH GPU DIAGNOSTIC")
print("=" * 70)

try:
    import torch
    print(f"\n✓ PyTorch installed: {torch.__version__}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"✓ CUDA version: {torch.version.cuda}")
        print(f"✓ GPU device: {torch.cuda.get_device_name(0)}")
        print(f"✓ Number of GPUs: {torch.cuda.device_count()}")
        
        # Test tensor on GPU
        x = torch.randn(3, 3).cuda()
        print(f"✓ Successfully created tensor on GPU!")
        print("\n🎉 PyTorch is properly configured for GPU!")
    else:
        print("\n⚠ CUDA is NOT available!")
        print("\nReasons this could happen:")
        print("  1. PyTorch CPU-only version is installed")
        print("  2. No NVIDIA GPU detected")
        print("  3. NVIDIA drivers not installed")
        print("  4. CUDA toolkit not installed")
        
        print("\n💡 To install PyTorch with CUDA support:")
        print("   Visit: https://pytorch.org/get-started/locally/")
        print("\n   For CUDA 11.8:")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        print("\n   For CUDA 12.1:")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        
except ImportError:
    print("\n✗ PyTorch is not installed!")
    print("\nTo install PyTorch:")
    print("  pip install torch torchvision torchaudio")

print("\n" + "=" * 70)
