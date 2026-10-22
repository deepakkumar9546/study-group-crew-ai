# Python Object-Oriented Programming (OOP) — Final Study Guide

---

## Section 1: Research

### 1.1 Research Summary

The reviewed material provides an introduction to Python Object-Oriented Programming, covering the core vocabulary (classes, objects, attributes, methods) and the five pillars of OOP (inheritance, encapsulation, polymorphism, abstraction).

Key research findings from the reviewed notes:

- **Class**: A blueprint for creating objects; defines attributes and methods.
- **Object (Instance)**: A concrete realization of a class.
- **Instance Attributes**: Unique to each object; typically set via `self`.
- **Class Attributes**: Shared across all instances; set directly in the class body.
- **Methods**: Functions defined inside a class.
- **Inheritance**: A child class derives from a parent class.
- **Encapsulation**: Restricts access via naming conventions and name mangling.
- **Polymorphism**: Different classes treated via the same interface; commonly via method overriding.
- **Abstraction**: Hiding complex details; implemented in Python via the `abc` module.

### 1.2 Important Facts Gathered from the Reviewed Material

1. Everything in Python is generally treated as an object (integers, strings, functions, modules, classes).
2. `self` is a convention, not a keyword.
3. `__init__` is an initializer, not a true constructor; object creation actually happens in `__new__`.
4. Dunder (double-underscore) methods enable special behavior and operator overloading.
5. `super()` calls parent-class methods.
6. `isinstance()` and `issubclass()` are built-in type-checking functions.

### 1.3 Source References (as listed in the material)

- Python Official Documentation: https://docs.python.org/3/tutorial/classes.html
- Python Data Model: https://docs.python.org/3/reference/datamodel.html
- PEP 8: https://pep8.org/
- Real Python OOP Tutorials: https://realpython.com/python-oop/
- Python `abc` module: https://docs.python.org/3/library/abc.html

> **Uncertainty note:** Web search tools were unavailable during the research session, so live verification against current sources could not be performed. The assessments in Section 4 are therefore based on the reviewed material and established Python documentation, and should be treated as informed rather than freshly verified.

---

## Section 2: Explanation

### 2.1 Classes and Objects

A **class** is a blueprint; an **object** is an instance of that class.

```python
class Dog:
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

buddy = Dog("Buddy", 5)
```

### 2.2 Instance Attributes vs. Class Attributes

| Type | Definition | Access | Example |
|---|---|---|---|
| Instance Attribute | Defined in `__init__` via `self` | Unique per instance | `self.name` |
| Class Attribute | Defined in class body | Shared by all instances | `species = "Canis familiaris"` |

### 2.3 Methods

- **Instance method**: takes `self`, works on one instance.
- **Class method**: uses `@classmethod`, takes `cls`, bound to the class.
- **Static method**: uses `@staticmethod`, takes neither `self` nor `cls`.

### 2.4 Inheritance

- Single inheritance: child inherits from one parent.
- Multiple inheritance: child inherits from multiple parents; resolved via **MRO** (Method Resolution Order).
- Multilevel and hierarchical inheritance also exist.

### 2.5 Encapsulation

Python uses naming conventions:

- Public: no underscore (`name`)
- Protected: single underscore (`_name`) — convention only
- Private: double underscore (`__name`) — triggers name mangling (`_ClassName__name`)

### 2.6 Polymorphism

Different classes can be treated through a common interface; the common case is **method overriding**.

### 2.7 Abstraction

Python uses the `abc` module (`ABC` + `@abstractmethod`) for abstract base classes.

---

## Section 3: Quiz

> **Note:** No quiz questions were included in the reviewed source material. The following quiz was constructed from the reviewed content and should be treated as a self-test rather than an authoritative assessment.

### Question 1
What is the difference between a class and an object?

**Answer:** A class is a blueprint/template; an object is an instance of that class. No instance memory is allocated until an object is created (though defining the class itself creates the class object).

### Question 2
What does `__init__` do, and is it a true constructor?

**Answer:** `__init__` is an initializer that runs automatically when an object is created and sets up attributes. It is **not** a true constructor; the actual creation happens in `__new__`.

### Question 3
How do instance attributes differ from class attributes?

**Answer:** Instance attributes are unique to each object and set via `self`; class attributes are shared by all instances and set in the class body.

### Question 4
When would you use an instance method, a class method, and a static method?

**Answer:** Instance methods operate on instance data (`self`). Class methods operate on class-level data (`cls`) and use `@classmethod`. Static methods do not depend on instance or class state and use `@staticmethod`.

### Question 5
What is method overriding?

**Answer:** A child/subclass provides a specific implementation of a method already defined in its parent/superclass.

### Question 6
How does Python implement encapsulation, and is `__private` truly private?

**Answer:** Python uses naming conventions (`_protected`, `__private`) and name mangling. It is a convention, not strict enforcement like Java/C++.

### Question 7
What is polymorphism in Python OOP?

**Answer:** The ability of different classes to be treated as instances of a common type and respond to the same method call, typically through overriding.

### Question 8
How is abstraction implemented in Python?

**Answer:** Through the `abc` module using Abstract Base Classes and the `@abstractmethod` decorator.

### Question 9
Is `self` a keyword in Python?

**Answer:** No. `self` is a strong convention; technically any name could be used, though `self` is standard.

### Question 10
What are dunder methods?

**Answer:** Special methods with double underscores (e.g., `__init__`, `__str__`, `__repr__`, `__len__`, `__add__`) that enable special behavior and operator overloading.

---

## Section 4: Fact-Checking Notes

### 4.1 Claims Reviewed

| Claim from Reviewed Material | Assessment | Notes |
|---|---|---|
| `__init__` is automatically called when a new object is created | ✅ Supported | Correct; it initializes attributes. |
| `__init__` is a true constructor | ❌ Corrected | It is an initializer; `__new__` handles creation. |
| `self` is a convention, not a keyword | ✅ Supported | Correct. |
| Private attributes (`__`) are truly private | ❌ Corrected | Misconception; name mangling makes access harder but not impossible. |
| Inheritance should be used frequently | ❌ Corrected | Misconception; "favor composition over inheritance" is preferred. |
| All methods need `self` | ❌ Corrected | Misconception; class/static methods differ. |
| OOP makes code automatically better | ❌ Corrected | Misconception; design quality matters more. |
| Python doesn't support real encapsulation | ❌ Corrected | Misconception; Python uses conventions + properties. |
| Everything in Python is an object | ✅ Supported | Generally consistent with Python data model. |
| Multiple inheritance supported; MRO resolves methods | ✅ Supported | Correct. |
| When a class is defined, no memory is allocated until an object is created | ⚠️ Nuanced | Technically, the class object itself is allocated at definition; instances are allocated at instantiation. The intent is broadly understood but the wording is imprecise. |

### 4.2 Corrections Applied

- The material correctly identified several misconceptions and corrected them. These corrections align with established Python guidance.
- The statement that no memory is allocated until an object is created was flagged as slightly imprecise: defining a class allocates memory for the class object itself; instance memory is allocated when an object is instantiated.

### 4.3 Unverified or Uncertain Claims

- Practical applications (Tkinter, Django, Flask, Pygame, scikit-learn, Pandas, design patterns) are plausible but were not deeply verified in this session.
- Claims about "Python being designed to be object-oriented from the ground up" are broadly reasonable but should be understood alongside Python's multi-paradigm nature.

### 4.4 Verification Status

- Live web verification was unavailable during this review.
- Therefore, no claim should be treated as newly verified against current sources in this session.
- Unsupported or unverified claims should not be presented as confirmed facts.

---

## Section 5: Key Takeaways

- Python OOP uses **classes** as blueprints and **objects** as instances.
- `self` refers to the instance and is a convention, not a keyword.
- `__init__` initializes; `__new__` creates.
- Instance attributes are per-object; class attributes are shared.
- Use `@classmethod`, `@staticmethod`, or instance methods appropriately.
- Inheritance supports reuse; MRO handles multiple inheritance.
- Encapsulation uses naming conventions and name mangling, not strict privacy.
- Polymorphism is commonly achieved through method overriding.
- Abstraction uses `abc` and abstract methods.
- OOP is a tool, not a requirement; use it when it improves organization and clarity.

---

## Final Note

This study guide consolidates the reviewed material on Python OOP, includes a quiz with answers, and documents fact-checking decisions. Clear errors were corrected where identified, and uncertain or unverifiable claims were flagged. No unsupported fact has been presented as verified.