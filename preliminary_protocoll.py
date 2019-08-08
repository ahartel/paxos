from router import Router


class PreliminaryPriest:
    def __init__(self):
        pass

    def receive(self, message):
        pass


def create_priests(num):
    priests = []
    for n in range(num):
        priests.append(PreliminaryPriest())
    return priests


def main():
    priests = create_priests(5)
    router = Router()
    for priest in priests:
        router.add(priest)


if __name__ == '__main__':
    main()
