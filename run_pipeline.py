import sys
import os
import time

# Reconfigure stdout to use UTF-8, preventing charmap encoding errors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure sub-project folders are on the python path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(workspace_dir, "laboratuvar-projeleri", "bioinformatics-pipeline"))
sys.path.append(os.path.join(workspace_dir, "laboratuvar-projeleri", "eeg-processing-core"))
sys.path.append(os.path.join(workspace_dir, "laboratuvar-projeleri", "bci-motor-imagery"))

def print_banner():
    """Prints a beautiful high-fidelity ASCII Art banner for the terminal dashboard."""
    cyan = "\033[96m"
    magenta = "\033[95m"
    green = "\033[92m"
    yellow = "\033[93m"
    reset = "\033[0m"
    bold = "\033[1m"
    
    ascii_art = f"""
{cyan}    ____  _        _   __                      
   / __ )(_)___   / | / /__  __  ___________  
  / __  / / __ \ /  |/ / _ \/ / / / ___/ __ \ 
 / /_/ / / /_/ // /|  /  __/ /_/ / /  / /_/ / 
/_____/_/\____//_/ |_/\___/\__,_/_/   \____/  
                                              
     {magenta} _   __                     __                  __                  
     / | / /__  __  ___________  / /____  _________  / /___  ____ ___  __ 
    /  |/ / _ \/ / / / ___/ __ \/ __/ _ \/ ___/ __ \/ / __ \/ __ `/ / / / 
   / /|  /  __/ /_/ / /  / /_/ / /_/  __/ /__/ / / / / /_/ / /_/ / /_/ /  
  /_/ |_/\___/\__,_/_/   \____/\__/\___/\___/_/ /_/_/\____/\__, /\__, /   
                                                          /____//____/    {reset}
    """
    print(ascii_art)
    print(f"{bold}{green}[*] Biyo-Nöroteknoloji Bütünleşik Mühendislik Portalı ve Test Süreci{reset}")
    print(f"{yellow}[*] Sürüm: 1.0.0 | Uçtan Uca Hesaplamalı Sistemler Entegrasyonu\n{reset}")
    print("-" * 75)

def main():
    # Setup terminal colors if on Windows (ensure ANSI escape sequences are parsed)
    if sys.platform == 'win32':
        os.system('color')
        
    print_banner()
    
    try:
        # 1. Run Bioinformatics Pipeline
        print("\033[94m[ADIM 1] MOLEKÜLER BİYOLOJİ VE BİYOENFORMATİK ANALİZ HATTI ÇALIŞTIRILIYOR...\033[0m")
        time.sleep(1.0)
        from main import execute_bioinformatics_pipeline
        execute_bioinformatics_pipeline()
        
        # 2. Run EEG Processor Pipeline
        print("\033[94m[ADIM 2] BİYOMEDİKAL SİNYAL İŞLEME VE DİJİTAL FİLTRE HATTI ÇALIŞTIRILIYOR...\033[0m")
        time.sleep(1.0)
        from processor import execute_eeg_processing_pipeline
        execute_eeg_processing_pipeline()
        
        # 3. Run BCI Deep Learning Training Pipeline
        print("\033[94m[ADIM 3] BEYİN-BİLGİSAYAR ARAYÜZÜ (EEGNet) YAPAY ZEKÂ EĞİTİM HATTI ÇALIŞTIRILIYOR...\033[0m")
        time.sleep(1.0)
        from model import execute_bci_training_pipeline
        execute_bci_training_pipeline(epochs=5, batch_size=16)
        
        print("\033[92;1m[✓] TEBRİKLER! TÜM HESAPLAMALI BİYO-NÖROTEKNOLOJİ MODÜLLERİ HATA VERMEDEN BAŞARIYLA TAMAMLANDI!\033[0m")
        print("-" * 75)
        
    except ImportError as e:
        print(f"\033[91;1m[X] Hata: Bağımlılıklar veya modüller yüklenemedi. Detay: {e}\033[0m")
        print("\033[93m[!] Lütfen gerekli paketleri yüklediğinizden emin olun (pip install numpy scipy torch biopython)\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91;1m[X] Çalışma zamanı hatası oluştu: {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
