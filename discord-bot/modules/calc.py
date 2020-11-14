#!/usr/bin/env python


'''
Python で書いた関数電卓プログラムです。
動的型付けと関数オブジェクトを使うと簡潔に書けます。
'''


import math, re, sys, operator





class Operator:
   u'''演算子と定数のクラスです'''

   # 演算子の優先度。大きい方から優先的に計算される
   P_CST=6                                 # 定数の優先度
   P_LHB=5                                 # ! の優先度
   P_FUN=4                                 # 関数の優先度
   P_POW=3                                 # 累乗の優先度
   P_UPM=2                                 # 単項の + と - の優先度
   P_MD=1                                  # *, /, % の優先度
   P_BPM=0                                 # ２項の +, - の優先度


   def __init__(self, name, fun, priority):
       self.name=name
       self.fun=fun
       self.priority=priority

   def __call__(self, x=None, y=None):
       return self.fun        if self.is_const() else                    \
              self.fun(x)     if self.is_unary() or self.is_lhb() else   \
              self.fun(x, y)

   def __gt__(self, other):
       u'''self が other より優先度が高いとき True を返す'''
       assert other is None or isinstance(other, Operator)
       return other is None or \
         self.priority > other.priority or \
         ( self.priority in (Operator.P_FUN, Operator.P_POW, Operator.P_UPM) and self.priority == other.priority)

   def __str__(self):
       return self.name

   def __repr__(self):
       return repr(self.name)

   def is_const(self):
       return self.priority==Operator.P_CST

   def is_lhb(self):
       return self.priority==Operator.P_LHB

   def is_upm(self):
       return self.priority==Operator.P_UPM

   def is_func(self):
       return self.priority==Operator.P_FUN

   def is_unary(self):
       return self.priority in (Operator.P_FUN, Operator.P_UPM)

   def is_binary(self):
       return self.priority in (Operator.P_POW, Operator.P_MD, Operator.P_BPM)



# 関数

def is_natural(n):
   u'''自然数？'''
   return type(n) is int and n>=0



def fact(n):
   u'''階乗'''
   assert is_natural(n)
   return reduce(operator.__mul__, range(1, n+1)) if n>0 else 1



def permutation(m,n):
   u'''順列'''
   assert is_natural(m) and is_natural(n) and m>=n
   return reduce(operator.__mul__, range(m-n+1, m+1), 1)



def combination(m,n):
   u'''組み合わせ'''
   assert is_natural(m) and is_natural(n) and m>=n
   return permutation(m,n)/fact(n)





# 演算子と定数の辞書。
# 文字列をキーとし、対応する関数と優先度のタプル または 対応する定数を値にとる。
L_OP= [ \
 Operator('@+', operator.__pos__, Operator.P_UPM), \
 Operator('@-', operator.__neg__, Operator.P_UPM), \
 Operator('+', operator.__add__, Operator.P_BPM),\
 Operator('-', operator.__sub__, Operator.P_BPM), \
 Operator('*', operator.__mul__, Operator.P_MD),\
 Operator('/', operator.__truediv__, Operator.P_MD), \
 Operator('%', operator.__mod__, Operator.P_MD), \
 Operator('<<', operator.__lshift__, Operator.P_POW), \
 Operator('>>', operator.__rshift__, Operator.P_POW), \
 Operator('**', math.pow, Operator.P_POW), \
 Operator('^', math.pow, Operator.P_POW), \
 Operator('exp', math.exp, Operator.P_FUN), \
 Operator('log', math.log, Operator.P_FUN), \
 Operator('log10', math.log10, Operator.P_FUN), \
 Operator('sqrt', math.sqrt, Operator.P_FUN),  \
 Operator('abs', operator.__abs__, Operator.P_FUN), \
 Operator('sin', math.sin, Operator.P_FUN), \
 Operator('cos', math.cos, Operator.P_FUN), \
 Operator('tan', math.tan, Operator.P_FUN), \
 Operator('asin', math.asin, Operator.P_FUN), \
 Operator('acos', math.acos, Operator.P_FUN), \
 Operator('atan', math.atan, Operator.P_FUN), \
 Operator('!', fact, Operator.P_LHB), \
 Operator('P', permutation, Operator.P_POW), \
 Operator('C', combination, Operator.P_POW), \
 Operator('pi', math.pi, Operator.P_CST), \
 Operator('e', math.e, Operator.P_CST), \
    ]

# 演算子の名前をキーにしてハッシュ表を作る
H_OP=dict([(str(op), op)  for op in L_OP])


def convert_op_name(op):
   u'''演算子を正規表現文字列に変換して返す'''

   return ''.join([(c if c.isalnum() else '\\'+c) for c in str(op)]) + \
            (r'(?=\W|$)' if op.is_const() else r'(?=[\s\(])' if op.is_func() else '')



# 式の要素を表す正規表現
RE_FORM = re.compile( \
r'''(?P<nest>\()                                            |   # 入れ子
   (?P<num>\d+(?P<after_dot>\.\d+)?(?:[eE][+-]?\d+)?)      |   # 数値
   (?P<op_name>%s)                                             # 演算子
''' % ('|'.join([ convert_op_name(op)  for op in sorted([op for op in L_OP if not op.is_upm()], key=lambda x:len(str(x)), reverse=True)]),), \
re.VERBOSE)




# ツール
def cons(obj, ls):
   u'''Lisp 風にするため'''
   ls.append(obj)
   return ls



def operator_position (ls):
   u'''ls の中で最初に計算する演算子の位置を返す'''

   tprev, term0, pos = None, None, -1

   for i, term in enumerate(ls):
       if isinstance(term, Operator) and (term > term0 or (isinstance(tprev, Operator) and term.is_upm())):
           term0, pos = term, i
       tprev=term

   return term0, pos



def eval_ls(ls):
   u'''数値と演算子からなるリストを計算して結果を返す'''

   if operator.isNumberType(ls): return ls   # 数値ならそれを返す
   elif len(ls)==1:
       i=ls[0]
       return eval_ls(i() if isinstance(i, Operator) else i)    # 要素が１つのリストならそれを取り出す
   else:
       op, pos =operator_position(ls)  # 最初の使う演算子を探す

       if op.is_const(): # 定数
           return eval_ls(cons(op(), ls[:pos]) + ls[pos+1:])

       elif op.is_unary() and pos < len(ls)-1: # 単項演算子
           return eval_ls(cons(op(eval_ls(ls[pos+1])), ls[0:pos]) + ls[pos+2:])

       elif op.is_lhb() and pos>0: # !
           return eval_ls(cons(op(eval_ls(ls[pos-1])), ls[0:pos-1]) + ls[pos+1:])

       elif op.is_binary() and 0 < pos < len(ls)-1: # 二項演算子
           return eval_ls(cons(op( eval_ls(ls[pos-1]), eval_ls(ls[pos+1]) ), ls[0:pos-1]) + ls[pos+2:])

       else:
           raise RuntimeError, "invalid formmula: (%r)" % (ls,)

def find_pair(s0):
   u'''対応する閉じ括弧を探す'''
   n=0
   for i, c in enumerate(s0):
       if c in '()': n+= (1 if c=='(' else -1)
       if n==0: return i
   else:
       raise RuntimeError, "Cannot find the close parenthesis!"



def read_str(str):
   u'''文字列を読み込んで、数値と演算子のリストを返す'''
   def _iter(s, ls):
       s=s.strip()
       if(s):
           obj=RE_FORM.match(s)
           if obj and obj.group('nest'):
               idx=find_pair(s)
               return _iter(s[idx+1:], cons(_iter(s[1:idx], []), ls))
           elif obj:
               s1=s[obj.end():]
               if obj.group('num'):
                   return _iter(s1, cons((float if obj.group('after_dot') else int)(obj.group('num')), ls))
               else:
                   op_name = obj.group('op_name')
                   if op_name in '+-' and  (not ls or (isinstance(ls[-1], Operator) and not ls[-1].is_lhb())):   # 単項の +/- を識別する
                       op_name = '@' + op_name
                       return _iter(s1, cons(H_OP[op_name], ls))
            else:
               raise RuntimeError, "Cannot parse input!"
       else:
           return ls

   return _iter(str, [])



if __name__=='__main__':

   interactive= len(sys.argv)>1 and sys.argv[1]=='-i'
   if interactive:
       sys.stderr.write("Available operators and constants:\n" + \
                        ', '.join([str(op) for op in L_OP if not op.is_upm()]) + \
                        "\nq:quit\n\n")

   while(1):
       if interactive: sys.stderr.write('> ')
       str=sys.stdin.readline()
       if str:
           str=str.rstrip()
           if interactive and str=='q': break
           try:
               print eval_ls(read_str(str))
           except Exception,  strerror:
               print strerror
       else:
           break
