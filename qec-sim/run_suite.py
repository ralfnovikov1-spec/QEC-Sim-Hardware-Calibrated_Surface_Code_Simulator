import os
import time

def main():
    print("==================================================")
    print("   QEC-SIM: SCIENTIFIC RESEARCH SUITE v1.0")
    print("==================================================")
    print("Initializing environment...")
    
    # Ensure results dir exists
    if not os.path.exists("results"):
        os.makedirs("results")

    start = time.time()
    
    # Run Experiments
    os.system("python experiments/benchmark_google_vs_ibm.py")
    os.system("python experiments/benchmark_hybrid.py")
    os.system("python audit/omega_audit.py")
    
    print("\n==================================================")
    print(f"✅ SUITE COMPLETE in {time.time()-start:.2f}s")
    print("   Artifacts generated in /results")
    print("==================================================")

if __name__ == "__main__":
    main()
