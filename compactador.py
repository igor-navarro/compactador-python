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


def listar(arquivo):
    if arquivo.endswith(".tar.gz"):
        with tarfile.open(arquivo, "r:gz") as tf:
            itens = [(m.name, m.size) for m in tf.getmembers() if m.isfile()]
    else:
        with zipfile.ZipFile(arquivo) as zf:
            itens = [(i.filename, i.file_size) for i in zf.infolist() if not i.is_dir()]
    for nome, tamanho in itens:
        print(f"{tamanho:>10} bytes  {nome}")
    print(f"\n{len(itens)} arquivo(s)")


parser = argparse.ArgumentParser(description="Compactador simples (ZIP e TAR.GZ)")
sub = parser.add_subparsers(dest="cmd", required=True)

c = sub.add_parser("compactar")
c.add_argument("pasta")
c.add_argument("saida")

e = sub.add_parser("extrair")
e.add_argument("arquivo")
e.add_argument("destino")

l = sub.add_parser("listar")
l.add_argument("arquivo")

args = parser.parse_args()
if args.cmd == "compactar":
    compactar(args.pasta, args.saida)
elif args.cmd == "extrair":
    extrair(args.arquivo, args.destino)
else:
    listar(args.arquivo)