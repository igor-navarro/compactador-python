import argparse
import tarfile
import zipfile
from pathlib import Path


def compactar(pasta, saida):
    pasta = Path(pasta)
    if saida.endswith(".tar.gz"):
        with tarfile.open(saida, "w:gz") as tf:
            for arquivo in pasta.rglob("*"):
                if arquivo.is_file():
                    tf.add(arquivo, arcname=str(arquivo.relative_to(pasta)))
    else:
        with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zf:
            for arquivo in pasta.rglob("*"):
                if arquivo.is_file():
                    zf.write(arquivo, arquivo.relative_to(pasta))
    print(f"Criado: {saida}")


def extrair(arquivo, destino):
    if arquivo.endswith(".tar.gz"):
        with tarfile.open(arquivo, "r:gz") as tf:
            tf.extractall(destino)
    else:
        with zipfile.ZipFile(arquivo) as zf:
            zf.extractall(destino)
    print(f"Extraído em: {destino}")


parser = argparse.ArgumentParser(description="Compactador simples (ZIP e TAR.GZ)")
sub = parser.add_subparsers(dest="cmd", required=True)

c = sub.add_parser("compactar")
c.add_argument("pasta")
c.add_argument("saida")

e = sub.add_parser("extrair")
e.add_argument("arquivo")
e.add_argument("destino")

args = parser.parse_args()
if args.cmd == "compactar":
    compactar(args.pasta, args.saida)
else:
    extrair(args.arquivo, args.destino)