#!/usr/bin/python3

def ListDiff(li1, li2):
    return(list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def ListDiff1(li1, li2):
    return(list(set(li1)-set(li2)))

def ListDiff2(li1, li2):
    return(list(set(li2)-set(li1)))

def main():
    print("test code only")

    spidr_grp    = ['10.86.52.75', '10.86.52.84', '10.10.10.10']
    spidr_input  = ['10.86.52.75', '10.10.10.10']

    print("just a diff")
    print(ListDiff(spidr_grp, spidr_input))
    print("-------------------------------------------")

    print("Remove from Group")
    print(ListDiff1(spidr_grp, spidr_input))

    print("Add to Group")
    print(ListDiff2(spidr_grp, spidr_input))

    sick_grp   = ['10.86.53.10', '10.86.53.11', '10.86.53.12', '10.86.53.13', '10.86.53.21', '10.86.53.26', '10.86.53.27', '10.86.53.28', '10.86.53.29', '10.86.53.30', '10.86.53.31', '10.86.53.51', '10.86.53.52', '10.86.53.53', '10.86.57.197', '10.86.56.198', '10.86.57.198', '10.86.56.199', '10.86.57.199', '10.86.56.200', '10.86.57.200', '10.86.56.201', '10.86.57.201', '10.86.56.212', '10.86.57.212', '10.86.56.213', '10.86.57.213', '10.86.56.214', '10.86.57.214']
    sick_input = ['40.40.40.40', '10.86.53.10', '10.86.53.11', '10.86.53.12', '10.86.53.13', '10.86.53.21', '10.86.53.26', '10.86.53.27', '10.86.53.28', '10.86.53.29', '10.86.53.30', '10.86.53.31', '10.86.53.51', '10.86.53.52', '10.86.53.53']

    print("Remove from Group")
    print(ListDiff1(sick_grp,sick_input))
    print("add to group")
    print(ListDiff2(sick_grp,sick_input))


if __name__ == "__main__":
    main()
#end