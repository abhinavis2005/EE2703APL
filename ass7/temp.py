import numpy as np
from matplotlib import pyplot as plt

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


def populate_samples(Nsamp, mics, dist_per_samp, obstacle_location, sincP):

    samples = []
    for mic in mics:
        distance = dist((0, 0), obstacle_location, mic)
        distance_samples = []
        for i in range(Nsamp):
            distance_samples.append((i * dist_per_samp - distance))
        samples.append(wsrc(np.array(distance_samples) / C, sincP))
    return np.array(samples)


def reconstruct(samples, pitch, dist_per_samp, Nsamp):
    nmics = len(samples)


    miclist = []
    start = pitch / 2

    for i in range(Nmics // 2):
        miclist.append(start + i * pitch)
        miclist.append(-start - i * pitch)

    # if Nmics is odd, all mics moved up by pitch/2 and then an additional mic added at the bottom.
    if Nmics % 2 == 1:
        miclist = [mic + pitch / 2 for mic in mics]
        miclist.append(-(Nmics // 2) * pitch)
    mics.sort()

    y_coordinates = mics.copy()
    


    final_array = []
    for j in y_coordinates:
        x_vals = []
        for i in range(Nsamp // 2):
            measured_value = 0
            mic_index = 0
            for mic_y in miclist[:Nmics]:
                expected_distance = dist((0, 0), (i * dist_per_samp, j), mic_y)
                index = int(expected_distance / dist_per_samp)
                if index < len(samples[0]):
                    measured_value += samples[mic_index][index]
                mic_index += 1
            x_vals.append(measured_value)
        final_array.append(x_vals)
    return final_array


if __name__ == "__main__":
    Nmics = 64
    Nsamp = 200
    src = (0, 0)
    obstacle_location = (3, -1)
    # spacing between microphones
    pitch = 0.1
    dist_per_samp = 0.1
    C = 2.0
    sincP = 5
    obstacle = (3, -1)

    mics = populate_mics(Nmics, pitch)
    samples = populate_samples(Nsamp, mics, dist_per_samp, obstacle_location, sincP)
    for sample, i in enumerate(samples):
        plt.plot(sample+i)
    plt.savefig('timeplot.png', dpi = 300, bbox_inches = "tight")
    plt.clf()
    plt.imshow(samples)
    plt.savefig('heatmap.png', dpi = 300, bbox_inches = "tight")
    # plt.imshow(samples)

    reconstructed = reconstruct(samples, pitch, dist_per_samp, Nsamp)
    plt.imshow(reconstructed)
    plt.show()
    # plt.savefig("images/img9.png", dpi=300, bbox_inches="tight")

