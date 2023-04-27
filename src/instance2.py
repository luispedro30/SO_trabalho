class MyInstance:
    def __init__(self, I, J, dj, fi, si, cij, xij, yi):
        """Facility

        Attributes:
            I:  Number of Clients
            J:  Number of Facilities
            dj: Demand of Client j
            fi: Opening cost of facility i
            si: Maximum capacity of facility
            cij:Transportation cost between client j and facility i
            xij:If client j is assigned to facility i
            yi: If facility is open
        """
        self.I = I
        self.J = J
        self.dj = dj
        self.fi = fi
        self.si = si
        self.cij = cij
        self.xij = xij
        self.yi = yi 
     
# Create an object of the class using the default constructor
obj1 = MyInstance(2,2,2,[1,2],2,2,2,[0,2])

 
# Call a method of the class
print(obj1.yi)
dj = [j for j in obj1.yi]
print(dj)