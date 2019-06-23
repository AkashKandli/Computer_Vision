import cv2
import circles as circ
import time


cap = cv2.VideoCapture("ball_video.mp4")
ret, frame = cap.read()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi',fourcc, 20.0, (frame.shape[1], frame.shape[0]))
frames = 0
sTime = time.time()




while(True):
    # Capture frame-by-frame
    x  = time.time()
    ret, frame = cap.read()

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect circles in the frame with hough transform
    circles = circ.HoughTransformCircleOptimized(gray, 10, 40, 15)

    #built in opencv hough transform
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50,
    #                                             param1=50, param2=100, minRadius=0, maxRadius=0)

    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
    #                             param1=100, param2=40, minRadius=0, maxRadius=0)


    # draw detected circles on the frame
    for c in circles:
        # print("Radius:{}".format(c.r))
        # draw the outer circle
        cv2.circle(frame, (c.x, c.y), c.r, (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(frame, (c.x, c.y), 2, (0, 0, 255), 3)

    # draw circles (if using build in function)
    # circles = np.uint16(np.around(circles))
    # for i in circles[0, :]:
    #     # draw the outer circle
    #     cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #     # draw the center of the circle
    #     cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # write frame to output video
    output.write(frame)

    # Increment and display number of frames written to output video
    frames+= 1
    print("Frame Written:{}".format(frames))
    print("time->", time.time() - x)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Check total time elapsed
totalTime = time.time() - sTime
print(totalTime)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()