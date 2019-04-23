from snapshot import GeoDescribe

def main():

    # Load GeoDescribe
    geodescribe = GeoDescribe()

    # Take a picture
    while 1:
        output = geodescribe.snap()
