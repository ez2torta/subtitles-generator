# Subtitle Generator

Subtitle Generator is a simple and easy-to-use Python application that can generate subtitle images from text, remove silence from MP4 files, and even provide text-to-speech (TTS) capabilities with an external API.

It is meant for creators that want basic subtitles as images, without having to deal with one-by-one convertion or paid/limited services. 

## Features

1. **Subtitle Generation**: Paste your text in the provided text field, select the "Subtitles" mode, and click "Run". The application will generate PNG images for each line of text and save them in a timestamped folder.
2. **Silence Removal**: Drag and drop your MP4 file into the application, select the "Remove Silence" mode, and click "Run". The application will output a series of MP3 files, each containing a non-silent segment from the original audio.
3. **Text-to-Speech**: Coming soon! This feature will utilize the Azure voice Microsoft Text-to-Speech API to convert your text into speech.

## How to Use

1. Open the application.
2. For Subtitle Generation, paste your text in the text field at the top.
3. For Silence Removal, use the "Select MP4 file" button to choose your file.
4. Select your desired mode from the drop-down menu.
5. Click "Run" to execute the chosen operation.

You can customize the look of the subtitle directly into the code itself.

## Future Enhancements

- Integration with Azure voice Microsoft Text-to-Speech API for Text-to-Speech feature.
- Option for open-source Text-to-Speech.
- Enhanced user interface with settings/customizations tab.


TODO: make subtitles.txt linked to text box? maybe or make the script directly gather text from the text box
TODO: silence remover needs to be able to work without those arguments, like the output folder, should be managed differently
TODO: subtitle generator should run at the click of the button