rainbow = []
max = 357
for nana in range(0, max//7):
    for go in range(0, max//5):
        num1 = nana*7+go*5
        if num1 > max:
            break
        for san in range(0, max//3):
            num2 = num1 + san*3
            if num2 < max and num2 not in rainbow:
                rainbow.append(num2)
print(sorted(rainbow))
print(len(rainbow))


