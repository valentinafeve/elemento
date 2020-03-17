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


## How is X?

X is Y
(Y){X;be;(amod{advmod})?;(nmod{\*})?}
(sustantivo|adj){nsubj;cop;(amod{advmod})?;(nmod{\*})?}

## What do X do?

X verb akk
verb{X;Akk}
verb{nsubj;dobj|\*{dobj}}

> Dado que se cumpla el patrón

verb{nsubj;!(dobj|\*{dobj})}
> Se encontró un sujeto tácito

## When X what?

X verb Y(temp)
verb{X;Y}
verb{nsubj;(nmod:tmod)}

## Where X did Y?

X verb (time preposition) Y(place)
Y{X;cop;case}
place{nsubj;cop;case}
