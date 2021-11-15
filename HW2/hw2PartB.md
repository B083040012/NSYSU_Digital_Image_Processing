---
title: DIP HW2 PartB Explain
tags: DIP
---

# DIP HW2 PartB Explain
![](https://i.imgur.com/gN0HRz1.png) ![](https://i.imgur.com/vJ0ZLZY.png)
*pirate_a*&*pirate_b*

## B.1 (Averaging Mask)
* *pirate_a* after averaging mask
![](https://i.imgur.com/Ay7TNKe.png)
* *pirate_b* after averaging mask
![](https://i.imgur.com/dHVK4yA.png)
* As we can see above,the noise of two image has both reduced,and there has no much difference between two de-noising image. 
* Effect of averaging mask's de-noising is limited because the difference of the pixels covered by mask can be very large.And after applying averaging mask,we merge the impact of both original image and noise together,so we discover there are still some noise in image.


## B.2 (3x3 Median Filter)
* *pirate_a* after 3x3 median filter
![](https://i.imgur.com/0hBfJak.png)
* *pirate_b* 3x3 after median mask
![](https://i.imgur.com/skIN8vF.png)
### Explain
* Unlike the averaging mask in B.1,median filter can directly choose the grayscale value that is close to the original image,so it can get better de-noising result compared with averaging mask.
* Why *pirate_b* still can't reach the better de-noising effect?
    * I think it's because the noise is too **dense** within *pirate_b*,so the grayscale value is more harder to be choosen by the median filter,leading to the result that doesn't seem to be much different compared with averaging mask.

## B.3 (Laplacian Mask)
```type
the laplacian mask I used
[[ 1, 1, 1],
[ 1,-8, 1],
[ 1, 1, 1]]
```
* *pirate_a_median* after laplacian mask
![](https://i.imgur.com/V09qawr.png)
* compare with the original *pirate_a* (without de-noising) after laplacian mask
![](https://i.imgur.com/56NDwF8.png)
### Explain
*Laplacian mask* is used for edge detecting,as we can see above,it's hard to detect the edge of *pirate_a*'s without any preprocessing.So I pick the image (*pirate_a applying median mask*) with the best de-noising effect,and according to the result above,we can clearly see that the edge has been correctly highlighed by the laplacian filter.
