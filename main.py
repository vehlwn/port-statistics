import argparse
import matplotlib.pyplot as plt
import re
import typing


Frequencies = typing.Dict[int, int]


def get_statistics(file, proto: str) -> Frequencies:
    ret: typing.Dict[int, int] = dict()
    port_re = re.compile(f" PROTO={proto} .* DPT=(\\d+)")
    for line in file:
        match = port_re.search(line)
        if match:
            port_num = int(match[1])
            ret[port_num] = ret.get(port_num, 0) + 1
    return ret


def prepare_data(
    f: Frequencies, top: int
) -> typing.Tuple[typing.List[str], typing.List[int]]:
    array_pairs = list(f.items())
    array_pairs.sort(key=lambda x: x[1], reverse=True)
    array_pairs = array_pairs[:top]
    array_pairs = array_pairs[::-1]
    print(array_pairs)
    return (
        list(map(lambda x: str(x[0]), array_pairs)),
        list(map(lambda x: x[1], array_pairs)),
    )


def plot_barchart(f: Frequencies, out_fname: str, top: int):
    x, y = prepare_data(f, top)
    plt.figure(figsize=(5, 10), dpi=300)
    plt.grid(linestyle="--", linewidth=1, axis="x", zorder=1)
    plt.barh(
        x,
        y,
        zorder=2,
    )
    plt.yticks(fontsize=4)
    plt.savefig(out_fname)


def main():
    parser = argparse.ArgumentParser(
        description="Draw port scan statistics from dmesg logs",
    )
    parser.add_argument(
        "-i",
        "--input-file",
        help="Name of an exported log file",
        required=True,
        type=argparse.FileType("rt", encoding="utf-8"),
    )
    parser.add_argument(
        "-p",
        "--protocol",
        help="L4 protocol with port field",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out_filename",
        help="File name of an output image",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--top",
        help="Top t popular ports",
        type=int,
        default=100,
    )
    args = parser.parse_args()
    ret = get_statistics(args.input_file, args.protocol)
    print(len(ret))
    plot_barchart(ret, args.out_filename, args.top)


if __name__ == "__main__":
    main()
