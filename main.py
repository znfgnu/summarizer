from PyTeaserPython3 import pyteaser

if __name__ == "__main__":
    print("Hello")
    url = "https://www.the-gazette.co.uk/news/17666505.european-elections-2019-snp-landslide-as-voters-abandon-labour/"
    result = pyteaser.SummarizeUrl(url)
    print(result)