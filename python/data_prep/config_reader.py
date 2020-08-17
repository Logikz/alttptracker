from configparser import ConfigParser


def read_config(filename, section):
    """
    Read a .ini configuration file
    :param filename: filename to the configuration file
    :param section: Section of the .ini file
    :return: Dictionary containing configuration for given file and section
    """
    parser = ConfigParser()

    if not parser.read(filename):
        raise Exception(f"{filename} is not found or contains no configuration")

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found within file {filename}")

    return config