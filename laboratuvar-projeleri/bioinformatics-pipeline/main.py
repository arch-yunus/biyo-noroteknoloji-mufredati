import os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def analyze_sequence(fasta_file):
    """
    Analyses a DNA sequence from a FASTA file.
    Calculates GC content and identifies basic patterns.
    """
    if not os.path.exists(fasta_file):
        print(f"Error: {fasta_file} not found.")
        return

    for record in SeqIO.parse(fasta_file, "fasta"):
        print(f"\n--- Sequence ID: {record.id} ---")
        seq = record.seq
        length = len(seq)
        gc_content = (seq.count("G") + seq.count("C")) / length * 100
        
        print(f"Length: {length} bp")
        print(f"GC Content: {gc_content:.2f}%")
        
        # Translate to Protein
        try:
            protein = seq.translate(to_stop=True)
            print(f"Protein Sequence (first 20 aa): {protein[:20]}...")
        except Exception as e:
            print(f"Translation Error: {e}")

        # Basic Variant Detection (Mock)
        # In a real scenario, this would compare against a reference genome
        print("Searching for potential CpG islands...")
        cpg_count = seq.count("CG")
        print(f"CpG count: {cpg_count}")

def generate_mock_data(output_file):
    """Generates a mock DNA sequence for testing."""
    mock_seq = "ATGC" * 100 + "GATC" * 50 + "CG" * 10
    record = SeqRecord(Seq(mock_seq), id="Mock_DNA_001", description="Synthetic sequence for testing")
    SeqIO.write(record, output_file, "fasta")
    print(f"Generated mock data: {output_file}")

if __name__ == "__main__":
    mock_file = "sample_data.fasta"
    generate_mock_data(mock_file)
    analyze_sequence(mock_file)
