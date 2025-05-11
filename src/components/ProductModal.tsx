import React from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { X } from 'lucide-react';

const productSchema = z.object({
  crystalType: z.enum(['60', '300', '980', '1980', '3280', '6480'], {
    required_error: 'Please select crystal amount'
  }),
  region: z.enum(['Europe', 'America', 'Asia', 'TW,HK,MO'], {
    required_error: 'Please select server region'
  }),
  uid: z.string()
    .min(9, 'UID must be at least 9 digits')
    .max(10, 'UID cannot exceed 10 digits')
    .regex(/^\d+$/, 'UID must contain only numbers'),
  quantity: z.number()
    .min(1, 'Minimum quantity is 1')
    .max(99, 'Maximum quantity is 99')
});

type ProductFormData = z.infer<typeof productSchema>;

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  product: {
    name: string;
    price: string;
  };
}

const detectRegion = (uid: string): 'Europe' | 'America' | 'Asia' | 'TW,HK,MO' | null => {
  const firstDigit = uid.charAt(0);
  const firstTwoDigits = uid.slice(0, 2);
  
  if (firstDigit === '7') return 'Europe';
  if (firstDigit === '6') return 'America';
  if (firstDigit === '8' || firstTwoDigits === '18') return 'Asia';
  if (firstDigit === '9') return 'TW,HK,MO';
  
  return null;
};

export function ProductModal({ isOpen, onClose, product }: ProductModalProps) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: {
      quantity: 1
    }
  });

  const quantity = watch('quantity');
  const crystalType = watch('crystalType');
  const uid = watch('uid');

  React.useEffect(() => {
    if (uid && uid.length > 0) {
      const region = detectRegion(uid);
      if (region) {
        setValue('region', region);
      }
    }
  }, [uid, setValue]);

  const calculatePrice = () => {
    const basePrice = parseInt(product.price.replace(/[^0-9]/g, ''));
    return new Intl.NumberFormat('fa-IR').format(basePrice * (quantity || 0)) + ' تومان';
  };

  const onSubmit = (data: ProductFormData) => {
    console.log('Form data:', data);
    // Handle add to cart logic here
    onClose();
  };

  return (
    <Dialog.Root open={isOpen} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm animate-fade-in" />
        <Dialog.Content className="fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] w-[90vw] max-w-[450px] rounded-lg bg-white p-6 shadow-xl focus:outline-none animate-slide-up">
          <div className="flex justify-between items-center mb-6">
            <Dialog.Title className="text-xl font-semibold text-gray-900">
              {product.name}
            </Dialog.Title>
            <Dialog.Close className="text-gray-400 hover:text-gray-500">
              <X className="h-5 w-5" />
            </Dialog.Close>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Crystal Amount
              </label>
              <select
                {...register('crystalType')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              >
                <option value="">Select amount</option>
                <option value="60">60 Crystals</option>
                <option value="300">300 Crystals</option>
                <option value="980">980 Crystals</option>
                <option value="1980">1,980 Crystals</option>
                <option value="3280">3,280 Crystals</option>
                <option value="6480">6,480 Crystals</option>
              </select>
              {errors.crystalType && (
                <p className="mt-1 text-sm text-red-600">{errors.crystalType.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Player UID
              </label>
              <input
                type="text"
                {...register('uid')}
                placeholder="Enter your 9-10 digit UID"
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
              {errors.uid && (
                <p className="mt-1 text-sm text-red-600">{errors.uid.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Server Region
              </label>
              <select
                {...register('region')}
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                disabled={!!uid && uid.length > 0 && !!detectRegion(uid)}
              >
                <option value="">Select region</option>
                <option value="Europe">Europe</option>
                <option value="America">America</option>
                <option value="Asia">Asia</option>
                <option value="TW,HK,MO">TW, HK, MO</option>
              </select>
              {errors.region && (
                <p className="mt-1 text-sm text-red-600">{errors.region.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Quantity
              </label>
              <input
                type="number"
                {...register('quantity', { valueAsNumber: true })}
                min="1"
                max="99"
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
              {errors.quantity && (
                <p className="mt-1 text-sm text-red-600">{errors.quantity.message}</p>
              )}
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center text-lg font-semibold">
                <span>Total Price:</span>
                <span className="text-primary">{calculatePrice()}</span>
              </div>
            </div>

            <button
              type="submit"
              className="w-full rounded-md bg-primary py-2 px-4 text-white hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-colors"
            >
              Add to Cart
            </button>
          </form>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}