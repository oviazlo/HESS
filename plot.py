from __future__ import print_function
import ROOT
from array import array
import sys
import math

from ROOT import TCanvas, TGraphAsymmErrors, TLegend, TF1
from ROOT import gROOT

########################################

def readDataIntoGraph():
	f=open('HESSj1745_290.dat',"r")
	lines=f.readlines()
	x, y, yHigh, yLow = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
	scaleFactor = 1000.0
	for iLine in lines:
		if iLine.isspace() == True or iLine[0] == '#':
			continue
		tmpList = iLine.split()
		x.append(scaleFactor*float(tmpList[0]))
		y.append(scaleFactor*float(tmpList[1]))
		yLow.append(scaleFactor*float(tmpList[2]))
		yHigh.append(scaleFactor*float(tmpList[3]))
	f.close()
	listOfZeros = array("d", [0] * len(x))
	gr = TGraphAsymmErrors(len(x),x,y,listOfZeros,listOfZeros,yLow,yHigh);
	#  gr.SetLineColor( color )
	gr.SetLineWidth( 2 )
	#  gr.SetMarkerColor( color )
	gr.SetMarkerStyle( 21 )
	gr.GetXaxis().SetTitle( 'Energy [GeV]' )
	gr.GetYaxis().SetTitle( 'dN/dE [cm^{-2}s^{-1}GeV^{-1}]' )
	gr.SetTitle('')
	return gr

########################################

c1 = TCanvas( 'c1', 'A Simple Graph Example', 200, 10, 600, 500 )
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
c1.Modified()
c1.Update()

leg = TLegend(0.7, 0.84, 0.9, 0.96)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)

dataGraph = readDataIntoGraph()
#  dataGraph.Draw("AP")

bkgFunc = TF1("bkg","[0]*[0]*pow(x,-[1])",0,10000)
bkgFunc.SetParameter(0,5.18e-4)
bkgFunc.SetParameter(1,2.8)
#  bkgFunc.Draw("same")
bkgFunc.Draw()

leg.AddEntry(dataGraph, 'exp. data', "lp");
leg.Draw("same")
c1.SetLogy()
c1.SetLogx()
c1.SaveAs('test.png')

