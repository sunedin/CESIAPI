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
                # print('initial sucess')

            except:
                print('Error: pyaimms is not installed properly')

            if cleanup:
                amplpy.AMPL().close()

            self.interface = amplpy.AMPL()
            self.interface_lowerlevel = self.interface

        if self.lang == 'Julia':

            try:
                import julia
                from julia import JuMP
                from julia import Main
                # print('Julia imported sucess')
            except:
                print('Error: Julia is not installed properly')

            j = julia.Julia()
            self.interface = JuMP
            self.jumpworkspace = Main
            self.interface_lowerlevel = self.jumpworkspace

        if self.lang == 'MATLAB':
            try:
                import matlab.engine
                # print('matlab.engine imported sucess')
                # print('matlab does not have object type of model, so using newmodel() point to the project folder of the matlab scripts, and leave modelfile paramter out')
            except:
                print('Error: matlab.engine is not installed properly')
            eng = matlab.engine.start_matlab()
            self.interface = eng
            self.interface_lowerlevel = eng

    # @classmethod
    def newmodel(self, modelfile=None, modelfolder=None, jumpmod_name = None):  # abs path
        """
        get model hanlder by Interpreting the specified file (script or model or mixed)

        Args:
            fileName: Full path to the file.

        Raises:
            RuntimeError: in case the file does not exist.
        """
        # modelfolder = os.path.realpath(os.path.join(os.getcwd(), modelfolder))
        # print('Current folder is {}'.format(modelfolder))
        # modelfile = os.path.realpath(os.path.join(os.getcwd(), modelfolder, modelfile))
        if self.lang == 'MATLAB':
            modelfile = None
            if not modelfolder or jumpmod_name or modelfile:
                print('please using modelfolder point to the project folder of the matlab scripts, and leave paramters as empty')
            self.interface_lowerlevel.addpath(self.interface_lowerlevel.genpath(os.path.abspath(modelfolder)))
            self.interface_lowerlevel.cd(os.path.abspath(modelfolder))

        # if modelfolder:
        #     modelfile = os.path.realpath(os.path.join(os.getcwd(), modelfolder, modelfile))
        # else:
        #     modelfile = os.path.realpath(os.path.join(os.getcwd(), modelfile))

        if self.lang == 'AMPL':
            if modelfolder:
                self.interface.cd(modelfolder)
            self.interface.read(modelfile)

        if self.lang == 'Julia':
            if not jumpmod_name:
                print('Please specify the name of interface model (as str) that defined in Julia file')
            # if modelfolder:
            #     self.interface_lowerlevel.cd(modelfolder)
            self.interface_lowerlevel.include(modelfile)
            self.jumpmod = getattr(self.jumpworkspace, jumpmod_name)
            print(self.jumpmod)




    # @classmethod
    # def getParam(cls, param):
    #
    #     pass
    #
    # @classmethod
    # def getVars(cls, *args):
    #     pass


    def getValue(self, Expression):
        """
        Get a value  from the underlying model, as a double or
        a string.

        .. note::
            for AMPL model, it is limited to scalar value and scalar expression. using getvalues for non-scalar value in AMPL

        Args:
            Expression: An expression which evaluates to a sclaar
            value.

        Returns:
            The value of the expression.
        """
        if self.lang == 'AMPL':
            try:
                s = self.interface.getValue(Expression)
            except:
                s = self.interface.getEntity(Expression).getValues().toDict()
            return s

        if self.lang == 'Julia':
            s = self.jumpworkspace.eval('getvalue({})'.format(Expression))
        return s

    def getValues(self, itemname):
        """
        Get a scalar value from the underlying model, as a double or
        a string.

        Args:
            Expression: An expression which evaluates to a scalar
            value.

        Returns:
            The value of the expression.
        """
        # todo: check
        # s = self.interface.getEntity(itemname).getValues().toDict()
        # return s
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
        s = self.interface.getSet(itemname)
        return s

    def setValues(self, itemname, values):
        """
        Get a scalar value from the underlying AMPL interpreter, as a double or
        a string.

        Args:
            Expression: An AMPL expression which evaluates to a scalar
            value.

        Returns:
            The value of the expression.
        """
        self.interface.getEntity(itemname).setValues(values)



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
        s = self.interface.getConstraint(itemname)
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
        s = self.interface.getParameter(itemname)
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
        s = self.interface.getVariable(itemname)
        return s

    def solve(self):

        """
         Solve the current model.

         Raises:
             RuntimeError: if the underlying interpreter is not running.
         """
        if self.lang == 'AMPL':
            s = self.interface.solve()

        if self.lang == 'Julia':
            s = self.interface.solve(self.jumpmod)
        return s

    def getObjectiveValue(self):
        """
        Get the the current objective. Returns `None` if no objective is set.

        """
        if self.lang == 'AMPL':
            s = self.interface.getCurrentObjective().getValues().toList()[0]
        if self.lang == 'Julia':
            s = self.interface.getobjectivevalue(self.jumpmod)
        return s

    def getObjectives(self):
        """
        Get all the objectives declared.
        """
        self.objs = [s[0] for s in self.interface.getObjectives()]
        print(self.objs)

    def eval(self, statement, *args, **kwargs):
        #todo: repoint self.JUMP to self.interface

        return self.interface_lowerlevel.eval(statement, *args, **kwargs)




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


    # model = MOD(lang='Julia')
    # model.newmodel(modelfile="planningmod.jl", modelfolder='julia_ampl\julia', jumpmod_name='rmp')
    # model.solve()
    # model.getObjectiveValue()
    # model.getValue('rmp[:x_inv][:]')
    # model.getValue('rmp[:cx]')
    #
    # model = MOD(lang='AMPL')
    # model.newmodel(modelfile="Operational-ini.run", modelfolder='julia_ampl/ampl/')
    # model.getSets()
    # model.getParams()
    # model.getConstraints()
    # model.solve()
    # model.getSet('sF')
    # model.getParam("pG_ub").getValue().toDict() #.to_markdown()
    # model.getConstraints('lambda_pG')
    # model.getConstraint('lambda_pG')
    # model.getValues('pG_ub')
    # model.setValues('pG_ub', {'Gnucl': 7000})
    # model.interface.getParameter('pG_ub').setValues({'Gnucl': 7700})
    # model.getParam("pG_ub").setValue()
    # model.getObjectiveValue()
    # model.getValue('oper')


    # for modelling languaging doesn't have object type of 'model'
    # it is possible to directly call a function or evaluate a statement, and return value to python
    model = MOD(lang='MATLAB')
    model.newmodel(modelfolder='../Newcastle')




    import pandas as pd
    import pprint as pp
    data = pd.read_excel("../Newcastle/Fdhn_Data_ogpf_datapackage.xlsx", sheet_name=None, header=1)
    data.keys()
    data['Bus Data']

    [SystemData, EN_SystemData, GN_SystemData] = model.interface.Read_Data("Fdhn_Data_ogpf_datapackage.xlsx", nargout=3)
    pp.pprint(EN_SystemData)
    results = model.interface.OGPF_Findhorn(EN_SystemData, GN_SystemData, SystemData, nargout=1)
    pp.pprint(results)
    pp.pprint(results['fval'])
    pp.pprint(results['lambda'])
    # pp.pprint(results['output']['message'])



    # data['GT specs'].loc[0, 'elec gen(MW)'] = 0.5
    # writer = pd.ExcelWriter('Fdhn_Data_ogpf_datapackage.xlsx')
    # for k, v in data.items():
    #     v.to_excel(writer, k, index=False)
    # writer.save()
    [SystemData, EN_SystemData, GN_SystemData] = model.interface.Read_Data("Fdhn_Data_ogpf_datapackage.xlsx", nargout=3)
    pp.pprint(EN_SystemData)
    results = model.interface.OGPF_Findhorn(EN_SystemData, GN_SystemData, SystemData, nargout=1)
    pp.pprint(results)
    pp.pprint(results['fval'])
    # pp.pprint(results['lambda'])
    # pp.pprint(results['output']['message'])
