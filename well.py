


class GravityWell(object):

    # Universal Gravitational Constant
    UGC = 6.67 / 10 ** 11

    def __init__(self, mass):
        self.mass = mass

    def escape_velocity(self, height):
        '''
        The velocity needed to escape at the given height
        '''
        return (2 * GravityWell.UGC * self.mass / height) ** (1.0 / 2.0)

    def pull(self, height):
        '''
        Gravitational pull of this well at the given height
        '''
        return GravityWell.UGC * self.mass / (height ** 2)

    def horizon(self, max_acceleration):
        '''
        Distance at which you won't be able to escape the pull of the planet
        with your acceleration. Unless you start with a high velocity
        '''
        return (GravityWell.UGC * self.mass / max_acceleration) ** (1.0 / 2.0)

    def satellite(self, height):
        '''
        Returns the required speed (perpendicular) that you must have to orbit
        this well at the given height
        '''
        return (GravityWell.UGC * self.mass / height) ** (1.0 / 2)



