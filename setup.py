from setuptools import setup, find_packages

setup(
    name="specter-medsec",
    version="1.0.0",
    author="Rajesh Kumar Selvam et al.",
    description="SPECTER: Quantum Adversarial Framework for Medical Imaging Security",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/specter-medsec/SPECTER",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0", "scipy>=1.10.0", "matplotlib>=3.7.0",
        "Pillow>=10.0.0", "scikit-learn>=1.3.0", "networkx>=3.1",
        "tqdm>=4.65.0", "pydicom>=2.4.0",
    ],
    extras_require={
        "quantum": ["qiskit>=0.44.0", "qiskit-aer>=0.12.0",
                    "qiskit-optimization>=0.6.0"],
        "dl": ["torch>=2.0.0", "torchvision>=0.15.0"],
        "all": ["qiskit>=0.44.0", "qiskit-aer>=0.12.0",
                "qiskit-optimization>=0.6.0",
                "torch>=2.0.0", "torchvision>=0.15.0"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
)
