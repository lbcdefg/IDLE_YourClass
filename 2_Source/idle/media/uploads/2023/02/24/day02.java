/*
package aa.bb; //��Ű�� ����

import java.lang.String; //java.lang ��Ű���� �ھ���Ű���� ���� import���ص� ��!
import java.lang.System; //����Ʈ ����(���� ����X) 

class A { //Ŭ�������� 
   String name; //�������(�Ӽ�)
   A(){//������
   }
   void m() { //�޼ҵ�(���)
   }
}
*/

package aa.bb; // package������ 1�� ���Ϸθ� ���𰡴�, ����Ʈ �������� ���� ���;��� (��������)
import java.lang.String; // Ŭ������������ �׻� ����Ʈ ������ ���� ���;��� (��������)

class A {      //Ŭ�������� �������� ��������X
   String name = "ȫ�浿"; //�ʱ�ȭ initializing, ù��° ���� �����͸� �ʱⰪ initial data / ��������� �Ұ�ȣ ����ϸ�ȵ�
   int age = 24;
   A(){
	   System.out.println("A()");
   }
   A(String.name){
	  this.name = name;          // �����ڰ� �� �̻��� �� ����, ��ȣ ���� �Ķ���ͷ� ����   �ۼ���ġ�� �������
   }
   void go() {
	   System.out.println("����");   //m()��� ���ٸ� �Է��ϸ� ���������� ȫ�浿�� ���ٰ� ����!
   }
   void eat() {
	   System.out.println("�Դ´�");   
   }
}

class Auser{
   public static void main(String args[]){
      A a1 = new A(); //��ü1 ����, �����ڸ޼��� �����ε�, ������ ȣ��ÿ��� �ݵ�� new�������
	  System.out.print("���̰� "+a1.age+"�� " + a1.name+"�� ");
	  a1.eat(); //���

	  A a2 = new A(); //��ü2 ����
	  System.out.print("���̰� "+ a2.age + "�� "+a2.name + "�� ");
	  a2.go(); //���
   }
}
