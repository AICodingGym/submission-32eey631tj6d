import astropy.units as u

class PoC(object):

    @u.quantity_input
    def __init__(self, voltage: u.V) -> None:
        pass

if __name__ == '__main__':
    try:
        poc = PoC(1.*u.V)
        print("Success!")
    except Exception as e:
        import traceback
        traceback.print_exc()
