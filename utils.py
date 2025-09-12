import zstandard as zstd

def compress_file(input_path, output_path, level=3):
    """
    Compress a file using Zstandard.
    
    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to save the compressed file.
        level (int): Compression level (1-22). Default is 3.
    """
    cctx = zstd.ZstdCompressor(level=level)
    with open(input_path, "rb") as fin, open(output_path, "wb") as fout:
        fout.write(cctx.compress(fin.read()))
