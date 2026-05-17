import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Standard genetic code mapping table
GENETIC_CODE = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAG':'K', 'AAA':'K',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAG':'E', 'GAA':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAG':'Q', 'CAA':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R'
}

def transcribe(dna_sequence):
    """Transcribes a DNA sequence into RNA (replaces Thymine with Uracil)."""
    return dna_sequence.upper().replace('T', 'U')

def reverse_complement(dna_sequence):
    """Generates the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    return "".join(complement.get(base, 'N') for base in reversed(dna_sequence.upper()))

def translate(dna_sequence):
    """Translates a DNA sequence into a protein sequence based on the standard genetic code."""
    dna = dna_sequence.upper()
    protein = []
    # Start at first codon
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]
        amino_acid = GENETIC_CODE.get(codon, 'X')
        if amino_acid == '_':  # Stop codon
            break
        protein.append(amino_acid)
    return "".join(protein)

def find_cpg_islands(sequence, window_size=100, step_size=10, min_gc=0.50, min_obs_exp=0.60):
    """
    Identifies CpG islands using a sliding window algorithm.
    A window is classified as a CpG island if:
      1. GC Content > min_gc (typically 50%)
      2. Observed/Expected ratio of CpG > min_obs_exp (typically 0.60)
    Obs/Exp = (Number of CpG * Window Length) / (Number of C * Number of G)
    """
    sequence = sequence.upper()
    islands = []
    
    for i in range(0, len(sequence) - window_size + 1, step_size):
        window = sequence[i:i+window_size]
        g_count = window.count('G')
        c_count = window.count('C')
        cpg_count = window.count('CG')
        
        # Calculate GC Content
        gc_content = (g_count + c_count) / window_size
        
        # Calculate Observed/Expected CpG Ratio
        if g_count > 0 and c_count > 0:
            obs_exp = (cpg_count * window_size) / (c_count * g_count)
        else:
            obs_exp = 0.0
            
        if gc_content >= min_gc and obs_exp >= min_obs_exp:
            islands.append({
                'start': i,
                'end': i + window_size,
                'gc_content': gc_content * 100,
                'obs_exp_ratio': obs_exp
            })
            
    return islands

def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap=-2):
    """
    Needleman-Wunsch algorithm for global sequence alignment (from scratch).
    """
    n, m = len(seq1), len(seq2)
    # Initialize score matrix
    score_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        score_matrix[i][0] = i * gap
    for j in range(m + 1):
        score_matrix[0][j] = j * gap
        
    # Fill score matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s_match = score_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            s_delete = score_matrix[i-1][j] + gap
            s_insert = score_matrix[i][j-1] + gap
            score_matrix[i][j] = max(s_match, s_delete, s_insert)
            
    # Traceback
    align1, align2 = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and (score_matrix[i][j] == score_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + gap:
            align1.append(seq1[i-1])
            align2.append("-")
            i -= 1
        else:
            align1.append("-")
            align2.append(seq2[j-1])
            j -= 1
            
    return "".join(reversed(align1)), "".join(reversed(align2)), score_matrix[n][m]

def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-2):
    """
    Smith-Waterman algorithm for local sequence alignment (from scratch).
    """
    n, m = len(seq1), len(seq2)
    # Initialize score matrix
    score_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    max_score = 0
    max_i, max_j = 0, 0
    
    # Fill score matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s_match = score_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            s_delete = score_matrix[i-1][j] + gap
            s_insert = score_matrix[i][j-1] + gap
            score_matrix[i][j] = max(0, s_match, s_delete, s_insert)
            
            if score_matrix[i][j] > max_score:
                max_score = score_matrix[i][j]
                max_i, max_j = i, j
                
    # Traceback
    align1, align2 = [], []
    i, j = max_i, max_j
    while i > 0 and j > 0 and score_matrix[i][j] > 0:
        score = score_matrix[i][j]
        diag = score_matrix[i-1][j-1]
        up = score_matrix[i-1][j]
        left = score_matrix[i][j-1]
        
        if score == diag + (match if seq1[i-1] == seq2[j-1] else mismatch):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif score == up + gap:
            align1.append(seq1[i-1])
            align2.append("-")
            i -= 1
        elif score == left + gap:
            align1.append("-")
            align2.append(seq2[j-1])
            j -= 1
            
    return "".join(reversed(align1)), "".join(reversed(align2)), max_score

def execute_bioinformatics_pipeline():
    """Runs a complete test suite of the bioinformatics pipeline."""
    print("==================================================")
    print("🧬 BIOPHYSICS & COMPUTATIONAL BIOLOGY PIPELINE")
    print("==================================================")
    
    # 1. Generate realistic synthetic sequence representing an oncogene with promoter (CpG island)
    promoter = "CGCGCG" * 15 + "ATATAT" * 10  # Rich in CG and TATA box
    coding_sequence = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGTTGGTATCA" # Part of Beta-Globin Gene
    dna_seq = promoter + coding_sequence
    
    print(f"\n[+] Generated Synthetic Gene Sequence (Length: {len(dna_seq)} bp)")
    print(f"    First 60 bp: {dna_seq[:60]}...")
    
    # 2. Transcription & Translation
    rna = transcribe(coding_sequence)
    protein = translate(coding_sequence)
    print(f"\n[+] Central Dogma Verification:")
    print(f"    - Coding DNA (first 30 bp): {coding_sequence[:30]}")
    print(f"    - Transcribed RNA:        {rna[:30]}...")
    print(f"    - Translated Protein:     {protein[:15]}...")
    
    # 3. CpG Island Discovery
    print("\n[+] Scanning for CpG Islands (Sliding Window: 100bp, Step: 10bp)...")
    islands = find_cpg_islands(dna_seq, window_size=100, step_size=10)
    if islands:
        print(f"    Found {len(islands)} CpG candidate windows:")
        for idx, island in enumerate(islands[:3]):
            print(f"    - Island {idx+1}: Position {island['start']}-{island['end']} | GC: {island['gc_content']:.1f}% | Obs/Exp: {island['obs_exp_ratio']:.2f}")
    else:
        print("    No CpG Islands found.")
        
    # 4. Pairwise Alignment Demonstration
    print("\n[+] Executing Sequence Alignment Algorithms from Scratch:")
    seq_ref = "ATGGTGCATCTGACTCCTGAGGAG"
    seq_mut = "ATGGTGCATCTGTCTCCTG-GGAG" # Mutation + Deletion
    
    print(f"    - Reference Seq: {seq_ref}")
    print(f"    - Mutant Seq:    {seq_mut}")
    
    # Global Alignment (Needleman-Wunsch)
    g_align1, g_align2, g_score = needleman_wunsch(seq_ref, seq_mut)
    print("\n    --> Needleman-Wunsch (Global Alignment):")
    print(f"        Ref: {g_align1}")
    print(f"        Mut: {g_align2}")
    print(f"        Global Score: {g_score}")
    
    # Local Alignment (Smith-Waterman)
    l_align1, l_align2, l_score = smith_waterman(seq_ref, seq_mut)
    print("\n    --> Smith-Waterman (Local Alignment):")
    print(f"        Ref: {l_align1}")
    print(f"        Mut: {l_align2}")
    print(f"        Local Score: {l_score}")
    print("==================================================\n")

if __name__ == "__main__":
    execute_bioinformatics_pipeline()
