from wait import waitcls

def simpleNumberRequest(promptMessage, promptCursor, options, lowerLimit, upperLimit, speedMode):
    while True:
        for i in range(len(options)):
            option = options[i].label
            print(i+1, '.', ' ', option, sep='')
        print(promptMessage)
        request = input(promptCursor)
        try:
            requestInt = int(request)
        except ValueError:
            waitcls(0, False)
            print('Non integer value entered!')
            waitcls(2, speedMode)
            continue
        if requestInt < lowerLimit or requestInt > upperLimit:
            print('Invalid option!')
            continue
        if type(requestInt) == int:
            return requestInt-1