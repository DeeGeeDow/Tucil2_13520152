zero = 10**-9

def twice_area(p_left, p_right, p):
  # return 2*area of triangle p_left-p_right-p
  # jika nilainya positif, p ada di atas garis p_left-p_right dan sebaliknya
  # jika posisinya ditukar (p_left ada di kanan, p_right ada di kiri), nilainya positif jika dan hanya jika p ada di bawah garis
  # perbandingan luas = perbandingan tinggi jika alasnya sama
  detval = p_left[0]*p_right[1] + p[0]*p_left[1] + p_right[0]*p[1] - p[0]*p_right[1] - p_right[0]*p_left[1] - p_left[0]*p[1]
  return detval

def ConvexHull(s):
    # return nx2 array, each row contains two indices of s which will be drawn a line that connects them
    if(len(s) == 0) : return [[]]

    simplices = []
    p_left = 0
    p_right = 0
    for i in range(len(s)):
      if(s[i][0]<s[p_left][0]): p_left = i
      elif(s[i][0]==s[p_left][0] and s[i][1]<s[p_left][1]): p_left = i
      if(s[i][0]>s[p_right][0]): p_right = i
      elif(s[i][0]==s[p_right][0] and s[i][1]>s[p_right][1]): p_right = i

    upper = []
    lower = []
    for i in range(len(s)):
      if(twice_area(s[p_left],s[p_right],s[i])>zero and i!=p_left and i!= p_right): upper.append(i)
      elif(twice_area(s[p_left],s[p_right],s[i])<zero and i!=p_left and i!=p_right): lower.append(i)
    
    simplices = qhull(s,upper,p_left,p_right) + qhull(s,lower,p_right,p_left)
    return simplices
  
def qhull(s, indices, p_left, p_right):
  # return nx2 array, each row contains two indices of s which will be drawn a line that connects them
  if(len(indices) == 0): return [[p_left, p_right]]
  else:
    farthest_point = indices[0]
    highest_tw_area = twice_area(s[p_left],s[p_right],s[farthest_point])
    for p in indices:
      tw_area = abs(twice_area(s[p_left],s[p_right],s[p]))
      if (tw_area>highest_tw_area or (abs(highest_tw_area - tw_area)<=zero and abs(s[p][0]-s[p_left][0]) < abs(s[farthest_point][0] - s[p_left][0]))) : 
        farthest_point = p
        highest_tw_area = tw_area
  
    left_points = []
    right_points = []
    for p in indices:
      if(twice_area(s[p_left],s[farthest_point],s[p])>zero and p!=p_left and p!=farthest_point):
        left_points.append(p)
      elif(twice_area(s[farthest_point],s[p_right],s[p])>zero and p!=p_right and p!=farthest_point):
        right_points.append(p)
    
    simplices = qhull(s,left_points,p_left,farthest_point) + qhull(s,right_points,farthest_point,p_right)
  
    return simplices