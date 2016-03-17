#!/usr/local/bin/python2.7
# encoding: utf-8
'''
pySMAC4SAT -- configuration for SAT

@author:     Stefan Falkner, Marius Lindauer

@copyright:  2015 AAD Group Freiburg. All rights reserved.

@license:   GPLv2

@contact:   {sfalkner,lindauer}@cs.uni-freiburg.de
'''

import os
import sys
import shutil
from pkg_resources import resource_filename

def generate_html(solver_name, meta, incumbent, test_perf, training_perf, param_imp_def, param_imp_not, plots, out_dir):
    '''
        generates a html website
        Args:
            solver_name: name of sat solver
            meta: list of meta_information (key, value)
            test_perf/training_perf: dictionary with keys: "par1", "par10", "tos" for "base" and "conf"
            parameter_importance: sorted list of (marginal,name)
            plots: dictionary with keys: "scatter", "cactus" and "fanova" (last one is a list of plots)
    '''
    
    header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
       "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Spying on %s</title>

<link href="css/lightbox.css" rel="stylesheet" />
<link href="css/accordion.css" rel="stylesheet" />
<link href="css/table.css" rel="stylesheet" />

<script src="js/jquery-1.11.0.min.js"></script>
<script src="js/lightbox.min.js"></script>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js"></script> 
<script type="text/javascript">
$(document).ready(function(){
    $("dt").click(function(){ // trigger 
        $(this).next("dd").slideToggle("fast"); // blendet beim Klick auf "dt" die nächste "dd" ein. 
        $(this).children("a").toggleClass("closed open"); // wechselt beim Klick auf "dt" die Klasse des enthaltenen a-Tags von "closed" zu "open". 
    });
});
</script>

</head>
<body>
<div id="wrapper">
<div id="container">
''' %(solver_name)
    
    footer = '''
</div>
</body>
</html>
'''
    plot_path = "./Plots/"

    with open(os.path.join(out_dir, "index.html"), "w") as fp:
        fp.write(header)
        
        fp.write("<h1>Spying on %s</h1>\n" %(solver_name))
        fp.write("Generated by <a href=\"http://www.ml4aad.org/spysmac/\"> SpySMAC </a> (S. Falkner, M. Lindauer and F. Hutter).\n")
        fp.write("<dl>\n")
        
        fp.write("<dt>Final Configuration <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n")
        #print(incumbent)
        fp.write("%s" %(" ".join("%s=%s" %(key, value) for key, value in list(incumbent.items()))))
        fp.write("</dd>\n")        
        
        #write meta data
        fp.write("<dt>Meta Data <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n")
        fp.write("<div class=\"Table\">\n")
        fp.write("<table>\n")
        fp.write("<tr><th>Solver</th><th>%s</th></tr>\n" %(solver_name))
        for key, value in meta:
            fp.write("<tr><th>%s</th><th>%s</th></tr>\n" %(key, value))
        fp.write("</table>\n")
        fp.write("</div>\n")
        fp.write("</dd>\n")
        
        
        # write Performance overview
        fp.write("<dt>Performance Overview <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n")
        fp.write("Test Performance\n")
        __write_html_stats_table(fp, test_perf)
        fp.write("<br><br>Training Performance\n")
        __write_html_stats_table(fp, training_perf)
        fp.write("</dd>\n")
        
        #Scatter Plot
        fp.write("<dt>Scatter Plot <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n <div align=\"center\">")
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Scatter Test Plot\" width=\"300px\"></a>\n" %
													   (plot_path + plots["scatter"]["test"],
                                                                                                            plot_path + plots["scatter"]["test"],
                                                                                                            plot_path + plots["scatter"]["test"],
                                                                                                            plot_path + plots["scatter"]["test"]))
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Scatter Train Plot\" width=\"300px\"></a>\n" % 
													(plot_path + plots["scatter"]["train"],
                                                                                                         plot_path + plots["scatter"]["train"],
                                                                                                         plot_path + plots["scatter"]["train"],
                                                                                                         plot_path + plots["scatter"]["train"]))
        fp.write("</div></dd>\n")
        
        # CDF Plot
        fp.write("<dt>CDF Plot <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n <div align=\"center\">")
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Cactus Plot\" width=\"300px\"></a>\n"  % 
													(plot_path + plots["cdf"]["test"],
                                                                                                         plot_path + plots["cdf"]["test"],
                                                                                                         plot_path + plots["cdf"]["test"],
                                                                                                         plot_path + plots["cdf"]["test"] ))
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Cactus Plot\" width=\"300px\"></a>\n"  % 
													(plot_path + plots["cdf"]["train"],
                                                                                                         plot_path + plots["cdf"]["train"],
                                                                                                         plot_path + plots["cdf"]["train"],
                                                                                                         plot_path + plots["cdf"]["train"] ))
        
        fp.write("</div></dd>\n")
        
        # Cactus Plot
        fp.write("<dt>Cactus Plot <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n")
        fp.write("<dd>\n <div align=\"center\">")
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Cactus Plot\" width=\"300px\"></a>\n"  % 
													(plot_path + plots["cactus"]["test"],
                                                                                                         plot_path + plots["cactus"]["test"],
                                                                                                         plot_path + plots["cactus"]["test"],
                                                                                                         plot_path + plots["cactus"]["test"] ))
        fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Cactus Plot\" width=\"300px\"></a>\n"  % 
													(plot_path + plots["cactus"]["train"],
                                                                                                         plot_path + plots["cactus"]["train"],
                                                                                                         plot_path + plots["cactus"]["train"],
                                                                                                         plot_path + plots["cactus"]["train"] ))
        
        __write_fanova(fp, param_imp_def, plots["fanova"]["DEFAULT"], "Default", plot_path)
        __write_fanova(fp, param_imp_not, plots["fanova"]["NOTHING"], "Nothing", plot_path)

        fp.write("</dl></div>\n")
        fp.write(footer)
    
    css_path = os.path.join(out_dir,"css")
    img_path = os.path.join(out_dir,"img")
    js_path = os.path.join(out_dir,"js")
    # delete old files
    if os.path.isdir(css_path):
        shutil.rmtree(css_path)
    if os.path.isdir(img_path):
        shutil.rmtree(img_path)
    if os.path.isdir(js_path):
        shutil.rmtree(js_path)        
    shutil.copytree(resource_filename("SpySMAC", 'web_files/css'), css_path)
    shutil.copytree(resource_filename("SpySMAC", 'web_files/img'), img_path)
    shutil.copytree(resource_filename("SpySMAC", 'web_files/js'), js_path)
    
def __write_html_stats_table(fp, perf):
    fp.write("<div class=\"Table\">\n")
    fp.write("<table>\n")
    fp.write("<tr><th></th><th>Default</th><th>Configured</th></tr>\n")
    fp.write("<tr><th>Average Runtime</th><th>%.2f</th><th>%.2f</th></tr>\n" %(perf["base"]["par1"], perf["conf"]["par1"]))
    fp.write("<tr><th>PAR10</th><th>%.2f</th><th>%.2f</th></tr>\n" %(perf["base"]["par10"], perf["conf"]["par10"]))
    fp.write("<tr><th>Timeouts</th><th>%d / %d</th><th>%d / %d</th></tr>\n" %(perf["base"]["tos"], perf["n"], perf["conf"]["tos"], perf["n"]))
    fp.write("</table>\n")
    fp.write("</div>\n")
    
def __write_fanova(fp, parameter_importance, plots, impr_over, plot_path):
    
    # Parameter Importance Plot
    fp.write("<dt>Parameter Importance (capped at %s) <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n" %(impr_over))
    fp.write("<dd>\n")
    if not parameter_importance:
        fp.write("fANOVA crashed - please see logfiles for further details.")
    else:
        fp.write("<div class=\"Table\">\n")
        fp.write("<table>\n")
        fp.write("<tr><th>Parameter</th><th>Importance</th></tr>\n")
        for marginal, parameter in parameter_importance:
            fp.write("<tr><th>%s</th><th>%.2f</th></tr>\n" %(parameter, marginal))
        fp.write("</table>\n")
        fp.write("</div>\n")
    fp.write("</dd>\n")
    
    fp.write("<dt>Parameter Importance Plots (capped at %s) <a href=\"#\" id=\"button\" class=\"closed\">Details</a></dt>\n" %(impr_over))
    fp.write("<dd>")
    if not parameter_importance:
        fp.write("fANOVA crashed - please see logfiles for further details.")
    else:
        fp.write("<div align=\"center\">\n")
        for fplot in plots:
            fp.write("<a href=\"%s\" data-lightbox=\"%s\" data-title=\"%s\"><img src=\"%s\" alt=\"Fanova Plot\" width=\"300px\"></a>\n"  % 
														(plot_path + fplot, 
														 plot_path + fplot, 
														 plot_path + fplot, 
												 		 plot_path + fplot))
        fp.write("</div>")
    fp.write("</dd>\n")
        
    
