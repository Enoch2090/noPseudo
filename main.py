import argparse
import MIPS_obj


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="File location")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.file != None:
        MIPS_object = MIPS_obj.MIPS_obj(args.file)
        MIPS_object.remove_pseudo(print_log=True)
        MIPS_object.to_file(args.file.replace(
            ".", "_translated."), print_log=True)
