# encoder-decoder <a href="https://www.buymeacoffee.com/parthmandaliya" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" align="right"></a>

This project serves as a Binary to Video Encoder and Decoder. It reads a given file as binary, converts the binary data into a NumPy array of type uint8 (essentially an ASCII array of the binary), and writes it as a video frame.

## Challenges and Considerations

The primary challenge in a project of this nature is that the output video can become significantly larger than the original file. This approach aims to address this issue effectively.

### Challenges:
- **Data Loss Risk:** Since the file is written as it is, any re-encoding of the video with a lossy codec may result in corrupted files.
- **Frame Size Dependency:** The amount of data each frame can handle directly depends on the frame size. Larger frames can accommodate more data.

## Recommendations

- **Encryption:** While not implemented in this version, it's recommended to use some encryption algorithm for added protection.
- **Compression:** Although the encoder creates the minimal video size possible, zipping the file or directory before encoding can yield better results in terms of reducing filesize. The effectiveness of this approach depends on the type of file being compressed.

## Note

- This encoder has not been extensively tested with zip files. If working with zip files, adjustments might be needed during decoding. Specifically, with the last frame, extra padding is added if the remaining data is insufficient to reshape the array to the frame size. If dealing with a zip file, consider truncating any remaining empty bytes before writing the zip file back to the disk.
