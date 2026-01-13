                                  Automated Sticker Placement Using Computer Vision

**Objectives**

Detect a shoebox from an image

Estimate the box orientation in the x–y plane

Compute the correct (x, y) pixel coordinates for sticker placement

Ensure the sticker position is fixed relative to the box, regardless of rotation

Visualize and save results for validation

*****Dataset*****

Since physical hardware (camera and box) was unavailable, a synthetic dataset was generated to accurately simulate a top-down conveyor belt scenario.

1.Dataset Characteristics:

Rectangular shoebox-like object
Flat background (conveyor belt simulation)
Multiple orientations (0°, 15°, 30°, 45°, 60°, 75°, 90°, 120°, 150°)

**Outputs**

For each input image, the system outputs:
1.Orientation angle (degrees)
2.Sticker placement pixel coordinates (x, y)
3.Annotated output image saved to disk

**Approach**
Image Preprocessing
Box Detection
Orientation Estimation
Sticker Placement Logic
Visualization--Green contour: detected box
               Blue line: orientation axis
               Red rectangle: sticker placement (rotated with box)
