#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Dr. W SUN on 15/04/2020

# -*- coding: utf-8 -*-

# import python libs

import os

# path = os.path.dirname(os.path.realpath(__file__))


class MOD():
    """
    Model is a Python wrapper around a submodel. It represents a Model+Solver object that can be instantiated with Data, solved and asked to return values + sensitivities
    """

    def __init__(self, lang, cleanup=True):

        self.lang = lang
        self.interface = None

        if self.lang == 'AMPL':
            try:
                import amplpy

            except:
                print('Error: pyaimms is not installed properly')

            if cleanup:
                amplpy.AMPL().close()
            self.interface = amplpy.AMPL()

    # @classmethod
    def newmodel(self, modelfile, modelfolder=''):  # abs path
        """
        get model hanlder by Interpreting the specified file (script or model or mixed)

        Args:
            fileName: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        os.chdir(modelfolder)
        self.interface.cd(modelfolder)
        # model = os.path.realpath(os.path.join(modelfolder, modelfile))
        # print('Current folder is {}'.format(modelfolder))

        if self.lang == 'AMPL':
            self.interface.read(modelfile)
        pass

    @classmethod
    def getParam(cls, param):

        pass

    @classmethod
    def getVars(cls, *args):
        pass

    @classmethod
    def getValue(cls, param):
        pass

    @classmethod
    def getConstraint(cls, param):
        pass



    def getSets(self):
        """
        Get all the sets declared.
        """
        self.sets = [s[0] for s in self.interface.getSets()]
        print(self.sets)

    def getSet(self, itemname):
        """
        Get the set with the corresponding name.

        Args:
            name: Name of the set to be found.

        Raises:
            TypeError: if the specified set does not exist.

        Return:
            a list with the dual data.
        """
        s = self.interface.getSet(itemname).getValues().toList()
        return s

    def getConstraints(self):
        """
         Get all the constraints declared.
         """
        self.Const = [s[0] for s in self.interface.getConstraints()]
        print(self.Const)

    def getConstraint(self, itemname):
        """
        Get the dual value of constraint with the corresponding name.

        Args:
            name: Name of the constraint to be found.

        Raises:
            TypeError: if the specified constraint does not exist.

        Return:
            a list with the dual data.
        """
        s = self.interface.getConstraint(itemname).getValues().toList()
        return s

    def getParams(self):
        """
        Get all the parameters declared.
        """
        self.Param = [s[0] for s in self.interface.getParameters()]
        print(self.Param)

    def getParam(self, itemname):
        """
        Get the parameter with the corresponding name.

        Args:
            name: Name of the parameter to be found.

        Raises:
            TypeError: if the specified parameter does not exist.
         """
        s = self.interface.getParameter(itemname).getValues().toDict()
        return s

    def getVars(self):
        """
        Get all the Variables declared.
        """
        self.Param = [s[0] for s in self.interface.getVariables()]
        print(self.Param)

    def getVar(self, itemname):
        """
        Get the variable with the corresponding name.

        Args:
            name: Name of the variable to be found.

        Raises:
            TypeError: if the specified variable does not exist.
         """
        s = self.interface.getVariable(itemname).getValues().toDict()
        return s

    def solve(self):

        """
         Solve the current model.

         Raises:
             RuntimeError: if the underlying interpreter is not running.
         """
        s = self.interface.solve()
        return s

    def getObjectiveValue(self):
        """
        Get the the current objective. Returns `None` if no objective is set.

        """
        s = self.interface.getCurrentObjective().getValues().toList()[0]
        return s

class data():
    """
    Data is used to represent any item of Data (or Parameter, or a variables) It can be indexed over one or several sets For the time being we could just support one-dimensional data
    """

    def __init__(self, ):
        """Constructor for data"""

    def dim(self):
        """
        List of pointers/reference to the sets used to index the data

        Returns:
            Number of indexing dimensions (given by sets)

        """
        pass

    def indices(self):
        """
        Access method to index sets.

        Returns:
            List of pointers/reference to the sets used to index the data
        """
        pass

    def type(self):
        """
        Access method to type identifier

        Returns:
            Name for the data (out of the predefined types if applicable), for example, "generator capacity", "line reactance"
        """
        pass

    def unit(self):
        """
        Access method to unit used by data.

        Returns:
            Unit (String consiting of numerical number + SI unit)

        """
        pass

    def setValues(self, identifiers, values):
        """
        Set (subset of) data to the given values.
        The data positions identified by the array of identifiers are set to the values given by the array values. The set identifiers consists of set elements of the original indexing set or to identifiers set up by the last associated Dictionary.

        Args:
            identifiers: Array of identifiers (as defined in indexing Set or Dictionary)
            values: Array of data values to be used.
        """
        pass

    def setDictionary(self, dict):
        """
        Associate dictionary with the data Sets up a dictionary for the data.

        .. note::
            The dictionary can define a subset of the data (together with an order) and possibly alternate names under which the values in the data can be accessed from the outside world Dictionaries are always defined with respect to the original names


        Args:
            dict: The Dictionary to be associated with the data

        """
        pass


class Dictionary():
    """
    A dictionary is used to translate between local names (for example, identifiers within a set) to the global names used outside of the set. It can be seen as defining aliases to provide a unified access to elements of a set between different models.

    To use a dictionary it will be associated with a given Set (or item of Data) and provides an alias under which to access the members of the Set (or the corresponding elements of the Data). A Dictionary can also be used to define a subset of elements of a set and an established order, so that in order to say get or set values of a Data item indexed over a set, only an array of values has to be passed and the (previously associated) dictionary will make clear which positions of the data are referenced and in which order

    In the simplest form a dictionary just consist of two sets of identifiers: one the local ones that are names to be used on the outside

    .. note::
        All the methods setting up a dictionary use a local Set (or a subset thereof). It might be useful if the (full) local set is passed to the constructor (contructing method) so that we can check if the subset condition holds. One could explicitly associate(?) such a Dictionary with the given Set so that the Dictionary can also be used to translate/alias that particular Set.
        Not sure if the constructing methods should be actual constructors or normal class methods (that fill in a previously constructed empty Dictionary)

    """

    def __init__(self, ):
        """Constructor for Dictionary """

    def fromLists(self, local, outside):
        """
        creates Dictionary from two explicit lists of identifiers.

        Args:
            local: array of local identifiers (must be element of an existing Set)
            outside: array of identifier names to be used on the outside
        """

    def fromSets(self, setlocal, setoutside):
        """
        creates Dictionary from two Set objects.

        Args:
            setlocal: Set (or subset) used locally
            setoutside: Set to be used on the outside (must be of same cardinality as the Set setlocal)
        """

class Set():
    """
    Set represents an indexing set used by any of the data or variables used in the model. This can be an abstract set declared in the model file without having any actual elements attached to it Unlike a mathematical Set, this Set object does imply an order
    """

    def __init__(self,):
        """Constructor for Set"""

    def clone(self):
        """
        Copy method that clones an existing set.

        Could be used as basis to construct changed names for a dictionary

        Returns:
            A cloned copy of the Set

        """
        pass

    def elements(self):
        """
        Access method to elements of the set.

        Returns:
            Reference to the elements of the set. Given as an array of strings

        """
        pass

    def matchreplace(self, regex):
        """
        perform a regex match and replace operation on all the names of the set

        Args:
            regex: The regular expression to be used

        """
        pass

    def name(self):
        """
        Access method to name.

        Returns:
            The name of the set (such as "Generators"). As defined in the AMPL like header of the Model

        """
        pass

    def subset(self, indices):
        """
        pick out given elements of a set (by removing the others)

        Args:
            indices: ordinal numbers of the elements to be retained (in the order in which they should be retained)

        """
        pass

    def subsetmatch(self, regex):
        """
        pick out elements of a set by performing a regex match (only keeps those elements that match a given regex, keepin the initial order of the remaining elements)

        Args:
            regex: The regular expression to be used

        Returns:

        """
        pass



if __name__ == '__main__':

    model = MOD(lang='AMPL')
    model.newmodel(modelfile="Operational-ini.run", modelfolder='julia_ampl/ampl/')
    model.getSets()
    model.getSet('sF')
    model.getConstraints()
    model.getParam("pG_ub") #.to_markdown()
    model.solve()
    model.getConstraints('lambda_pG')
    model.getConstraint('lambda_pG')
    print('nice work')
