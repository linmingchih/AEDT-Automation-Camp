# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0
# 8:25:07  Jul 30, 2020
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")

def chamfer(objname, edges):
    oEditor.Chamfer(
        [
            "NAME:Selections",
            "Selections:="		, objname,
            "NewPartsModelFlag:="	, "Model"
        ], 
        [
            "NAME:Parameters",
            [
                "NAME:ChamferParameters",
                "Edges:="		, edges,
                "Vertices:="		, [],
                "LeftDistance:="	, "0.02mm",
                "RightDistance:="	, "0.02mm",
                "ChamferType:="		, "Left Distance-Right Distance"
            ]
        ])

for obj in oEditor.GetSelections():
    faces = oEditor.GetFaceIDs(obj)
    data = []
    for i in faces:
        data.append((oEditor.GetFaceArea(i), i))
    data.sort(reverse = True)

    (_, f1), (_, f2) = data[0:2]
    v1 = oEditor.GetVertexIDsFromFace(f1)[0]
    x1, y1, z1 = oEditor.GetVertexPosition(v1)
    v2 = oEditor.GetVertexIDsFromFace(f2)[0]
    x2, y2, z2 = oEditor.GetVertexPosition(v2)
    
    topface = f1 if float(z1) > float(z2) else f2
    top_edges = oEditor.GetEdgeIDsFromFace(topface)
    
    data2=[(oEditor.GetEdgeLength(edge_id), edge_id) for edge_id in top_edges]
    data2.sort()
    (_, shortest1), (_, shortest2) = data2[0:2]
    top_edges.remove(shortest1)
    top_edges.remove(shortest2)
    AddWarningMessage(str(top_edges))
    chamfer(obj, map(int, top_edges))
    