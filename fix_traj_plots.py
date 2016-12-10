import os
import cv2
import matplotlib.pyplot as plt

for idx in range(10):
	print idx
	image = cv2.imread('data/0'+str(idx)+'/a_star_fake_experts.png')
	plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	plt.gca().invert_yaxis()
	plt.axis("off")
	plt.savefig('data/0'+str(idx)+'/a_star_fake_experts_fixed.png', bbox_inches='tight')
	plt.close()
