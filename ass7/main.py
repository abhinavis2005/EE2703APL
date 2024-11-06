import numpy as np
from matplotlib import pyplot as plt
import argparse


def dist(src: tuple, pt: tuple, mic: float) -> float:
    """
    function calculates distance from src to pt
    and from pt to mic, and returns their sum
    note that mic, is just the y coordinate of the mic
    (assuming mics are on the y axis)
    """
    d1 = np.sqrt(
        np.square(src[1] - pt[1]) + np.square(src[0] - pt[0])
    )  # distance from src to pt
    d2 = np.sqrt(
        np.square(mic - pt[1]) + np.square(0 - pt[0])
    )  # distance from pt to mic
    return d1 + d2


def wsrc(t: float, SincP: float) -> float:
    """
    returns sinc(sincP*t)
    """
    return np.sinc(SincP * t)


def populate_mics(Nmics: int, pitch: float) -> list:
    """
    function takes in Number of mics, pitch
    and returns a sorted array of microphones'
    y-coordinates
    """
    mics = []
    start = pitch / 2

    for i in range(Nmics // 2):
        mics.append(start + i * pitch)
        mics.append(-start - i * pitch)

    # if Nmics is odd, all mics moved up by pitch/2 and then an additional mic added at the bottom.
    if Nmics % 2 == 1:
        mics = [mic + pitch / 2 for mic in mics]
        mics.append(-(Nmics // 2) * pitch)
    mics.sort()

    return mics


def populate_samples(
    Nsampi: int,
    mics: list,
    dist_per_samp: float,
    obstacle_location: tuple,
    sincP: float,
) -> np.array:
    """
    This function generates a 2d matrix samples, corresponding to N samples
    for each microphone in the mics array
    """
    samples = []
    for mic in mics:
        distance = dist((0, 0), obstacle_location, mic)
        distance_samples = []
        for i in range(Nsamp):
            distance_samples.append(
                (i * dist_per_samp - distance)
            )  # the value of the function after subtracting the delay
        samples.append(wsrc(np.array(distance_samples) / C, sincP))
    return np.array(samples)


def reconstruct_big(
    samples: list, pitch: float, dist_per_samp: float, Nsamp: int
) -> float:
    """
    This function reconstructs the image from the samples from each mic,
    by considering the maximum possible y coordinate and x coordinate.

    """
    nmics = len(samples)

    miclist = populate_mics(nmics, pitch)

    y_coordinates = (
        []
    )  # array containing all the y coordinates for which we will evaluate DAS algorithm
    for i in range(
        1, int((Nsamp * dist_per_samp + (nmics // 2) * pitch) / (2 * pitch))
    ):
        y_coordinates.append(pitch * i)
        y_coordinates.append(-pitch * i)
    y_coordinates.append(0)

    y_coordinates.sort()

    final_array = [] # final reconsrtucted image array
    for j in y_coordinates:
        x_vals = []
        for i in range(Nsamp // 2):
            measured_value = 0 #value picked up by the mic
            mic_index = 0
            for mic_y in miclist:
                expected_distance = dist((0, 0), (i * dist_per_samp, j), mic_y)
                index = int(expected_distance / dist_per_samp) #index at which the expected value lies, with delay
                if index < len(samples[0]):
                    measured_value += samples[mic_index][index]
                mic_index += 1
            x_vals.append(measured_value)
        final_array.append(x_vals)
    return final_array


def reconstruct_small(samples, pitch, dist_per_samp, Nsamp):
    """
    This function reconstructs the image from the samples from each mic,
    where the x goes from 0 to Nsamp/2 but y coordinates corresponds to the 
    positions of the mics themselves. 
    """

    nmics = len(samples)

    miclist = populate_mics(nmics, pitch)

    y_coordinates = miclist.copy()

    final_array = []
    for j in y_coordinates:
        x_vals = []
        for i in range(Nsamp // 2):
            measured_value = 0 # actual signal picked up by the microphone
            mic_index = 0
            for mic_y in miclist:
                expected_distance = dist((0, 0), (i * dist_per_samp, j), mic_y) 
                index = int(expected_distance / dist_per_samp) #index of the value with delay
                if index < len(samples[0]):
                    measured_value += samples[mic_index][index]
                mic_index += 1
            x_vals.append(measured_value)
        final_array.append(x_vals)
    return final_array



if __name__ == "__main__":
    # change all the variables here
    Nmics = 64
    Nsamp = 200
    src = (0, 0)
    obstacle_location = (3, -1)
    pitch = 0.1
    dist_per_samp = 0.1
    C = 2.0
    sincP = 5
    obstacle = (3, -1)

    #taking in command line arguements
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", action="store_true", help="plot samples generated for parameters"
    )
    parser.add_argument("-r", action="store_true", help="reconstruct the data")
    parser.add_argument("-a", action="store_true", help="analyse the given text files")

    args = parser.parse_args()
    if args.c:
        # generate the plots for the given parameters
        mics = populate_mics(Nmics, pitch)
        samples = populate_samples(Nsamp, mics, dist_per_samp, obstacle_location, sincP)

        for sample, i in enumerate(samples):
            plt.plot(sample + i)
        plt.savefig("timeplot.png", dpi=300, bbox_inches="tight")
        plt.clf()
        plt.imshow(samples)
        plt.savefig("heatmap.png", dpi=300, bbox_inches="tight")
    if args.r:
        # reconstruct the image from the generated samples
        mics = populate_mics(Nmics, pitch)
        samples = populate_samples(Nsamp, mics, dist_per_samp, obstacle_location, sincP)
        reconstructed_image = reconstruct_small(samples, pitch, dist_per_samp, Nsamp)
        plt.clf()
        plt.imshow(reconstructed_image)
        plt.savefig("reconstructed_image.png", dpi=300, bbox_inches="tight")
    if args.a:
        # reconstruct images from the text files
        sample1 = np.loadtxt("rx2.txt")
        reconstructed_image = reconstruct_small(sample1, pitch, dist_per_samp, Nsamp)
        plt.clf()
        plt.imshow(reconstructed_image)
        plt.savefig("rx2.png", dpi=300, bbox_inches="tight")
        sample2 = np.loadtxt("rx3.txt")
        reconstructed_image = reconstruct_small(sample2, pitch, dist_per_samp, Nsamp)
        plt.clf()
        plt.imshow(reconstructed_image)
        plt.savefig("rx3.png", dpi=300, bbox_inches="tight")
