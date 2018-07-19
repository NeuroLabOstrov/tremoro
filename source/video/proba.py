matches = cv2.DMatch
list_kp1 = []
list_kp2 = []

for mat in matches:
    img1_idx = mat.queryIdx
    img2_idx = mat.trainIdx
    (x1, y1) = kp1[img1_idx].pt
    (x2, y2) = kp2[img2_idx].pt
    list_kp1.append((x1, y1))
    list_kp2.append((x2, y2))
