# Patterns

## Rules


x{y}
x tiene y como hijo

x|y
o se cumple x o y

x;y
x and y

!x
not x


## P01 - How is X?

X is Y
(Y){X;be;(amod{advmod})?;(nmod{\*})?}

(sustantivo|adj){nsubj;cop;(amod{advmod})?;(nmod{\*})?}

## P02 - What do X do?

X verb akk
verb{X;Akk}
verb{nsubj;dobj|\*{dobj}}

> Dado que se cumpla el patrón


## P03 - When X what?

X verb Y(temp)
verb{X;Y}
verb{nsubj;(nmod:tmod)}

## P04 - Where X did Y?

X verb (time preposition) Y(place)
Y{X;cop;case}
place{nsubj;cop;case}
