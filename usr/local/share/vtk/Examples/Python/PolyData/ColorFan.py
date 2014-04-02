#!/usr/bin/env python

import math
import vtk
import vtku

class ColorFan(object):
    def __init__(self, n_fins=24, opacity=1.0):
        # The complete fan:
        self.fan = vtk.vtkPolyData()

        # All the vertices of the fins of the fan:
        vertices = vtk.vtkPoints()

        # The common vertices of the fins on the z-axis:
        vertices.InsertPoint(0, (0.0, 0.0, -0.5))
        vertices.InsertPoint(1, (0.0, 0.0,  0.5))

        # All the polygons making up each fin:
        fins = vtk.vtkCellArray()

        # The angles of each fin in radians:
        angles = [2*math.pi*float(i)/float(n_fins) for i in range(n_fins)]

        # For each fin, compute the two vertices remote from the z-axis, and
        # insert a "cell" (rectangle) of the four vertices:
        for i,a in enumerate(angles):
            j = 2*i+2
            vertices.InsertPoint(   j, (math.cos(a), math.sin(a),  0.5) )
            vertices.InsertPoint( j+1, (math.cos(a), math.sin(a), -0.5) )
            fins.InsertNextCell( vtku.vtkIdList( (0,1,j,j+1) ) )

        # Add the vertices and polygons to the fan:
        self.fan.SetPoints(vertices)
        del vertices
        self.fan.SetPolys(fins)
        del fins

        # Set up a mapper for the fan:
        self.fanMapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.fanMapper.SetInput(self.fan)
        else:
            self.fanMapper.SetInputData(self.fan)

        # Color palette as a VTK lookup table:
        lut = vtku.X11Palette().asVtkLookupTable()
        n_colors = lut.GetNumberOfColors()
        self.fanMapper.SetScalarRange( 0, n_colors-1 )
        self.fanMapper.SetLookupTable( lut )

        # Set color indices for each fin:
        color_indices = [i%n_colors for i in range(n_fins)]
        self.fan.GetCellData().SetScalars( vtku.vtkIntArray(color_indices) )

        # Set up an actor:
        self.fanActor = vtk.vtkActor()
        self.fanActor.SetMapper(self.fanMapper)
        self.fanActor.GetProperty().SetOpacity(opacity)

    
    def getMapper(self):
        return self.fanMapper

    def getActor(self):
        return self.fanActor

    def getPolyData(self):
        return self.fan


def main():
    fan = ColorFan()

    # The usual (almost boilerplate for examples) rendering stuff.
    camera = vtk.vtkCamera()
    camera.SetPosition(1,1,1)
    camera.SetFocalPoint(0,0,0)

    renderer = vtk.vtkRenderer()
    renWin   = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renderer.AddActor( fan.getActor() )
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.SetBackground(1,1,1)

    renWin.SetSize(300,300)

    # interact with data
    renWin.Render()
    iren.Start()

main()

