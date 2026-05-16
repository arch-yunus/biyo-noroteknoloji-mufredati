# Modül 3: Biyoenformatik ve Hesaplamalı Biyoloji (Wet-to-Dry Lab)

Biyolojik verinin dijitalleştirilmesi, büyük veri analitiği ve yapay zeka tabanlı yapısal tahmin yöntemleri.

## ?? Öğrenme Hedefleri
* Dizi hizalama algoritmalarını (Smith-Waterman, Needleman-Wunsch) kodlamak ve analiz etmek.
* Yeni Nesil Sekanslama (NGS) verilerini işleme boru hatlarını (pipelines) kurmak.
* Protein yapısı tahmini ve moleküler yerleştirme (docking) simülasyonları gerçekleştirmek.

## ?? Temel Konular

### 1. Dizi Analizi ve Algoritmalar
* **Hizalama Yöntemleri:** Global (Needleman-Wunsch) ve lokal (Smith-Waterman) hizalama; dinamik programlama yaklaşımları.
* **BLAST (Basic Local Alignment Search Tool):** Hevristik arama yöntemleri ve istatistiksel anlamlılık (E-value).
* **Filogenetik Analiz:** Maksimum Olumluluk (Maximum Likelihood) ve Komşu Birleştirme (Neighbor-Joining) ağaçları.

### 2. Genomik ve Transkriptomik (NGS Veri Analizi)
* **Ham Veri İşleme:** FASTQ formatı, kalite kontrol (FastQC) ve okumaların (reads) referans genoma hizalanması (BWA, Bowtie2).
* **Varyant Analizi:** SNP (Tek Nükleotid Polimorfizmi) ve Indel tespiti (GATK boru hattı).
* **RNA-Seq:** Gen ifadesi analizi, diferansiyel gen ifadesi (DESeq2) ve tek hücre (single-cell) analizleri.

### 3. Yapısal Biyoloji ve İlaç Keşfi
* **Protein Yapısı Tahmini:** Homoloji modelleme ve derin öğrenme tabanlı yöntemler (AlphaFold2, RoseTTAFold).
* **Moleküler Dinamik (MD):** Newton kanunları ile moleküler hareketlerin simülasyonu (GROMACS, AMBER).
* **Moleküler Yerleştirme (Docking):** Ligand-protein etkileşimlerinin skorlanması ve ilaç adayı tarama (AutoDock Vina).

## ?? Yazılım ve Araç Seti
* **Python Kütüphaneleri:** `Biopython`, `Scanpy`, `Pandas`, `NumPy`.
* **Komut Satırı Araçları:** `samtools`, `bedtools`, `bcftools`.
* **Görselleştirme:** `UCSF ChimeraX`, `IGV (Integrative Genomics Viewer)`.

## ?? Önerilen Kaynaklar
* *Bioinformatics and Functional Genomics* - Jonathan Pevsner.
* *Structural Bioinformatics* - Jenny Gu, Bourne.
* *Python for Bioinformatics* - Sebastian Bassi.

---
> [!IMPORTANT]
> **Modül Projesi:** `laboratuvar-projeleri/bioinformatics-pipeline/` klasörü altında, ham sekans verisinden varyant analizi yapan örnek bir Python scripti bulunmaktadır.
