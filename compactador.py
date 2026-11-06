import argparse
import zipfile
from pathlib import Path


def compactar(pasta, saida):
    pasta = Path(pasta)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in pasta.rglob("*"):
            if arquivo.is_file():
                zf.write(arquivo, arquivo.relative_to(pasta))
    print(f"Criado: {saida}")


def extrair(zip_path, destino):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(destino)
    print(f"Extraído em: {destino}")


parser = argparse.ArgumentParser(description="Compactador simples")
sub = parser.add_subparsers(dest="cmd", required=True)

c = sub.add_parser("compactar")
c.add_argument("pasta")
c.add_argument("saida")

e = sub.add_parser("extrair")
e.add_argument("zip")
e.add_argument("destino")

args = parser.parse_args()
if args.cmd == "compactar":
    compactar(args.pasta, args.saida)
else:
    extrair(args.zip, args.destino)