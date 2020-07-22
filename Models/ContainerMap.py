class ContainerMap:
    FtpDirectory = ""
    ContainerIdentifierNumber = ""
    ContainerReferenceCode = ""
    ContainerFtpIdentifier = ""
    def __init__(self, ftpDirectory, containerIdentifierNumber, containerReferenceCode, containerFtpIdentifier):
        self.FtpDirectory = ftpDirectory
        self.ContainerIdentifierNumber = containerIdentifierNumber
        self.ContainerReferenceCode = containerReferenceCode
        self.ContainerFtpIdentifier = containerFtpIdentifier
