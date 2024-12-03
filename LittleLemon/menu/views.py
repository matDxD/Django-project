from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGestor, IsDeliveryCrew, IsClient
from rest_framework.decorators import api_view

# Clase para manejar los elementos del menú
class MenuItemList(APIView):
    def get(self, request):
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='Gestor').exists():
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Clase para manejar un solo detalle de un elemento del menú
class MenuItemDetail(APIView):
    def get(self, request, pk):
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.groups.filter(name='Gestor').exists():
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.groups.filter(name='Gestor').exists():
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vista basada en función para obtener todos los elementos del menú
@api_view(['GET'])
def menu_item_list(request):
    if request.user.groups.filter(name='Gestor').exists():
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

# Vista basada en función para manejar el detalle de un elemento específico
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def menu_item_detail(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if request.user.groups.filter(name='Gestor').exists():
            serializer = MenuItemSerializer(menu_item)
            return Response(serializer.data)
        else:
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

    if request.method in ['PUT', 'PATCH']:
        if not request.user.groups.filter(name='Gestor').exists():
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not request.user.groups.filter(name='Gestor').exists():
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
