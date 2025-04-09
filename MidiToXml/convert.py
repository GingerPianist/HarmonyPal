from music21 import *
import os

def convert_midi_to_musicxml(midi_path, output_path=None):
    """
    Convert a MIDI file to MusicXML format.

    Parameters:
    midi_path (str): Path to the input MIDI file
    output_path (str, optional): Path for the output MusicXML file.
                                If not provided, will use the same name as input with .xml extension

    Returns:
    str: Path to the generated MusicXML file
    """
    try:
        # Load the MIDI file
        midi_score = converter.parse(midi_path)

        # If no output path is specified, create one based on input file
        if output_path is None:
            base_name = os.path.splitext(midi_path)[0]
            output_path = f"{base_name}.xml"

        # Convert and save as MusicXML
        midi_score.write('musicxml', output_path)

        print(f"Successfully converted {midi_path} to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error converting file: {str(e)}")
        raise


def batch_convert_midi_folder(input_folder, output_folder=None):
    """
    Convert all MIDI files in a folder to MusicXML format.

    Parameters:
    input_folder (str): Path to folder containing MIDI files
    output_folder (str, optional): Path to folder for output MusicXML files.
                                  If not provided, will use the same folder as input

    Returns:
    list: List of paths to all generated MusicXML files
    """
    if output_folder is None:
        output_folder = input_folder

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    converted_files = []

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.mid', '.midi')):
            midi_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]
            xml_path = os.path.join(output_folder, f"{base_name}.xml")

            try:
                converted_file = convert_midi_to_musicxml(midi_path, xml_path)
                converted_files.append(converted_file)
            except Exception as e:
                print(f"Failed to convert {filename}: {str(e)}")
                continue

    return converted_files


# Example usage
if __name__ == "__main__":
    # Convert a single file
    midi_file = "path/to/your/file.mid"
    try:
        convert_midi_to_musicxml(midi_file)
    except Exception as e:
        print(f"Conversion failed: {str(e)}")

    # # Convert all files in a folder
    # midi_folder = "path/to/midi/folder"
    # xml_folder = "path/to/output/folder"
    # try:
    #     converted_files = batch_convert_midi_folder(midi_folder, xml_folder)
    #     print(f"Successfully converted {len(converted_files)} files")
    # except Exception as e:
    #     print(f"Batch conversion failed: {str(e)}")