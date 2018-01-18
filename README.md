# SegmentationCRF

Chinese word segmentation with CRF++.

## Running Environment

- Windows 10
- Python 3.6
- CRF++ 0.58

If running in a different environment, this program may not work properly.

For instance, considering the difference of newline between Windows and Linux, you need to modify Line 32 of `segment.py`.

## Usage

1. Prepare the correct environment mentioned above.
2. Run `python prepare.py`.
3. Prepare your own template for CRF++ or use `template.utf8` instead.
4. Run `CRF++-0.58/crf_learn.exe` (For Windows only) to train your own model or use the models in `CRF_Model/`.
5. Run `python segment.py` to segment.

## Test Result

Using the two models in `CRF_Model/`, the F1 Scores of testing files are listed as follows:

|       | crf_model_pku | crf_model_both |
|:---------:|:---------:|:---------:|
| pku_test | 0.931 | 0.880 |
| msr_test | 0.857 | 0.936 |

## Conclusion

Maybe adjusting the template and training parameters can make the result better, but as it takes too much time to do it, I just stop here.

Anyway, this is just the beginning of many to explore.
