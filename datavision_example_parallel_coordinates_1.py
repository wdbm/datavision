#!/usr/bin/python

import datavision

def main():

    data = [
        [0.9498061441975048, 0.6049394236952985, 5.168760062095979, 6.571102071810909, 0.3258710500404989],
        [0.6900900610786396, 0.044651963051884014, 5.6222021103273185, 6.413258445862534, 0.3989822610565017],
        [0.40245822087321015, 0.9000644399147708, 5.698656759965443, 5.706219545980181, 1.2501169295120753],
        [0.007788240630026866, 1.6630324065241182, 5.326062675832998, 6.198416367191167, 1.3785261503382713],
        [1.2329258057665577, 1.3760208006135484, 5.40272344446576, 5.697339583623006, 1.6475096314400532],
        [1.3736286937326467, 1.618862515954041, 5.9745190659395355, 5.252136196112335, 0.36162007500593485]
    ]

    datavision.save_parallel_coordinates_matplotlib(
        data,
        filename = "parallel_coordinates_1.png"
    )

if __name__ == "__main__":
    main()