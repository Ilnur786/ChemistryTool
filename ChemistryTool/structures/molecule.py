from .abc import MoleculeABC
from ..algorithms import Isomorphism


class Molecule(Isomorphism, MoleculeABC):
    def add_atom(self, element: str, number: int):
        if isinstance(element, str):
            self._atoms[number] = element
            self._bonds[number] = {}
        else:
            raise TypeError('нужно ввести строку')

    def add_bond(self, start_atom: int, end_atom: int, bond_type: int):
        if isinstance(start_atom, int) and isinstance(start_atom, int) and isinstance(start_atom, int):
            if start_atom == end_atom:
                raise KeyError('атом не может быть связан с сами собой')
            elif start_atom not in self._atoms or end_atom not in self._atoms:
                raise KeyError('таких атомов нет в словаре self._atoms')
            elif end_atom in self._bonds[start_atom]:  #проверка на то что существует ли связь
                raise KeyError('такая связь уже есть')
            else:
                self._bonds[start_atom].update({end_atom: bond_type})
                self._bonds[end_atom].update({start_atom: bond_type})
        else:
            TypeError('не числа')

    def __repr__(self):
        return 'Molecule: atoms{}, bonds{}'.format(self._atoms, self._bonds)


__all__ = ['Molecule']

