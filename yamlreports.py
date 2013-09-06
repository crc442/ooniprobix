# Base parser for OONIProbix
# Heavily modified from the example_parser.py script in the OONIProbe repo

# TO-DO: Look at the request headers.  Why they couldn't have stored them as
# dictionaries is beyond me.  Displaying this is a separete problem, but much
# more of a pain now.  
import yaml
import sys
import wx
import time

try:
    from yaml import CSafeLoader as Loader
except ImportError:
    print 'ImportError'
    from yaml import SafeLoader

#Written to close issue #12, this makes lists into a hashable type
#Taken from https://github.com/scooby/yaml_examples/blob/master/handle_mappings.py
def construct_mapping_kludge(loader, node):
    """ This constructor painfully steps through the node and checks
that each key is hashable. Actually, what it does is checks
whether it knows how to *make* it hashable, and if so, does that.
If not it just lets it through and hopes for the best. But the
common problem cases are handled here. If you're constructing
objects directly from YAML, just make them immutable and hashable! """
    def anything(node):
        if isinstance(node, yaml.ScalarNode):
            return loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            return loader.construct_sequence(node)
        elif isinstance(node, yaml.MappingNode):
            return construct_mapping_kludge(loader, node)
    def make_hashable(value):
        """ Reconstructs a non-hashable value. """
        if isinstance(value, list):
            return tuple(map(make_hashable, value))
        elif isinstance(value, set):
            return frozenset(value)
        elif isinstance(value, dict):
            return frozenset((make_hashable(key), make_hashable(val))
                             for key, val in value.items())
        else:
            return value
    def new_items():
        for k, v in node.value:
            yield (make_hashable(anything(k)), anything(v))
    return dict(new_items())
yaml.add_constructor(u'tag:yaml.org,2002:map', construct_mapping_kludge, Loader=Loader)

#print "Opening %s" % sys.argv[1]
#f = open(sys.argv[1])
#yamloo = yaml.safe_load_all(f)

# report_header = yamloo.next()
# for k in report_header:
# 	print k

def walk_dict(dictionary,tabs):
	ks = dictionary.keys()
	for k in ks:
		if type(dictionary[k]) is dict:
			print '\t' * tabs + k
			walk_dict(dictionary[k],tabs+1)
		elif type(dictionary[k]) is list:
			print '\t' * tabs + k
			walk_list(dictionary[k],tabs+1)
		else:
			print '\t' * tabs + k
		

def walk_list(lst,tabs):
	for l in lst:
		if type(l) is dict:
			walk_dict(l,tabs+1)
		elif type(l) is list:
			walk_list(l,tabs+1)
		else:
			pass
			if type(l) is str:
				if len(l) < 50:
					print '\t' * tabs + l
			else:
				print '\t' * tabs + l
				

# for report_entry in yamloo:
# 	ks = report_entry.keys()
# 	print '---'
# 	for k in ks:
# 		if type(report_entry[k]) is dict:
# 			print k
# 			walk_dict(report_entry[k],1)
# 		elif type(report_entry[k]) is list:
# 			print k
# 			walk_list(report_entry[k],1)
# 		else:
# 			print k
# 
# f.close()

# class YAMLReportTree(wx.TreeCtrl):
# 	def __init__(self):
# 		super(YAMLReportTree, self).__init__(*args, **kwargs)
# #		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpandItem)
# #		self.Bind(wx.EVT_TREE_ITEM_COLLAPSING,self.OnCollapseItem)
# 		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.OnItemActivated)
# 		self.__collapsing = False
# 
# 
# 	# Given a parent node, enumerate its children, noting whether or not
# 	# those children have child nodes too
# 
# 	# TO-DO: For purposes of this version, a node n "has children" if it is of
# 	# type dict and if len(n) > 0.  We'll handle lists later
# 	# REQUIRE: parent is a dict with at least one key 
# 
# 	def LoadYReport(self,yreport):
# 		#TO-DO: Change this to the name of the test, maybe with timestamp
# 		self.root = self.AddRoot(yreport.report_header['test_name'])
# 		self.SetItemHasChildren(root)
# 
# 		for entry in yreport.report_entries:
# 			tree_entry = self.AppendItem(root,wx.TreeItemData(entry))	
# 			self.SetItemHasChildren(tree_entry,False)
# #			EnumerateChildren(tree_entry,entry)
# 
# 
# 	def EnumerateChildren(self,wx_parent,parent):
# 			parent_keys = parent.keys()
# 			for key in parent_keys:
# 				child = self.AppendItem(self,parent=wx_parent,text=key,data=TreeItemData(parent[key]))
# 				if type(parent[key]) is type(parent[key]) is dict or type(parent[key]) is list or type(parent[key]) is set:
# 					self.SetItemHasChildren(child, len(parent[key]) > 0)
# 				else:
# 					self.SetItemHasChildren(child, False)
# 	
# 	def OnItemActivated(self,event):
# 		thing_to_print = str(self.GetPyData(event.GetItem()))
#                 dig = wx.MessageDialog(self, thing_to_print)
#                 dig.ShowModal()
#                 dig.Destroy()
# 		
# 
# 	def OnExpandItem(self,event):
# 		pass
# 
# 	def OnCollapseItem(self,event):
# 		pass
# #		if self.__collapsing:
# #			event.Veto()
# #		else:
# #			self.__collapsing = True
# #			item = event.GetItem()
# #			self.CollapseAllChildren(item)
# #			self.SetItemHasChildren(item)
# #			self.__collapsing = False

# class YAMLReportTreeFrame(wx.Frame()):
# 	def __init__(self, *args, **kwargs):
# 		super(YAMLReportTreeFrame, self).__init__(*args, **kwargs)
# 		self.__tree = YAMLReportTree(self)
		
#        def LoadYReport(self,yreport):
#                #TO-DO: Change this to the name of the test, maybe with timestamp
#                self.root = self.AddRoot(yreport.report_header['test_name'])
#                self.SetItemHasChildren(root)
#
#                for entry in yreport.report_entries:
#                        tree_entry = self.AppendItem(root,wx.TreeItemData(entry))
#			self.report_tree.SetPyData(tree_entry,(self.yfile.report_header[header_key],False))
#                        self.SetItemHasChildren(tree_entry,False)
#                       EnumerateChildren(tree_entry,entry)


#        def EnumerateChildren(self,wx_parent,parent):
#                        parent_keys = parent.keys()
#                        for key in parent_keys:
#                                child = self.AppendItem(self,parent=wx_parent,text=key)
				
#                                if type(parent[key]) is type(parent[key]) is dict or type(parent[key]) is list $
#                                        self.SetItemHasChildren(child, len(parent[key]) > 0)
#                                else:
#                                        self.SetItemHasChildren(child, False)
#constructor_loaded = False
class YAMLReport():

        def __init__(self, filename):
#                print 'Opening file for reading'


#                global constructor_loaded
#                if constructor_loaded == False:
#                    def construct_tuple(loader, node):
#                        return tuple(yaml.SafeLoader.construct_sequence(loader, node))
#                    yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:seq', construct_tuple)
#                    constructor_loaded = True

                i = 0
                f = open(filename,'r')
                #start_time = time.time()
#                print 'Calling yaml.safe_load_all'
#                yamloo = CSafeLoader(f).raw_parse()
#                cards = list(yaml.safe_load_all(f))
                yamloo = yaml.load_all(f, Loader=Loader)
#                print cards
#                print 'Call complete'
                #end_time = time.time()
		#print 'Call to yaml.safe_load_all() took %g seconds' % (end_time - start_time)
                self.report_name = filename
#                print 'Loading report header'
#                print type(yamloo)
                self.report_header = yamloo.next()
                self.report_entries = []
                
                for entry in yamloo:
#                    print 'Loading entry ' + str(i)
                    self.report_entries.append(entry)
                    i=i+1
#                print "Entries loaded.  It's all my parser code from here."
                f.close()
